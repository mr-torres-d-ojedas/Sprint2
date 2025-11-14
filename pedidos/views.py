from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.db import transaction
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum

from provesi.auth0backend import getRole
from .models import Pedido, Producto, EstadosPedido
from django.contrib.auth.decorators import login_required
from provesi.decorators import role_required
# from provesi.security import block_and_log, is_blocked

import time

def index(request):
    return render(request, "pedidos/index.html")

@login_required
@role_required(["TrabajadorBodega", "Gerente"])
def lista_pedidos(request):
    pedidos = Pedido.objects.prefetch_related('productos').all()
    return render(request, "pedidos/lista.html", {"pedidos": pedidos})

@csrf_exempt
@require_POST
@login_required
@role_required(["TrabajadorBodega"])  # este decorador ya permite entrar a TrabajadorBodega
def despachar_pedido(request, pedido_id):
    """Despacha un pedido validando versión (concurrencia) y estado."""

    # Verificación explícita y log en consola
    role = getRole(request)
    if role == "TrabajadorBodega":
        print(f"APROBADO: rol={role} puede despachar pedido {pedido_id}")
    else:
        print(f"DENEGADO: rol={role} no puede despachar pedido {pedido_id}")
        return JsonResponse({'success': False, 'message': 'No tiene permisos para despachar pedidos'}, status=403)

    # La versión llega por header o por body
    client_version = request.headers.get('X-Pedido-Version') or request.POST.get('version')
    try:
        client_version = int(client_version) if client_version is not None else None
    except ValueError:
        client_version = None

    try:
        with transaction.atomic():
            pedido = get_object_or_404(Pedido.objects.select_for_update(), id=pedido_id)
            # ...existing code...
            if client_version is not None and pedido.version != client_version:
                return JsonResponse({
                    'success': False,
                    'message': 'El pedido fue modificado por otro proceso. Intente recargar la página.'
                }, status=409)

            if pedido.estadoActual == EstadosPedido.DESPACHADO:
                return JsonResponse({'success': False, 'message': 'El pedido ya está despachado'}, status=400)

            anterior = pedido.estadoActual
            pedido.estadoActual = EstadosPedido.DESPACHADO

            hist = list(pedido.historialEstados or [])
            hist.append({
                "from": anterior,
                "to": pedido.estadoActual,
                "at": timezone.now().isoformat()
            })
            pedido.historialEstados = hist

            pedido.version = (pedido.version or 0) + 1
            pedido.save(update_fields=['estadoActual', 'historialEstados', 'version', 'updated_at'])

            return JsonResponse({
                'success': True,
                'message': f'Pedido #{pedido.id} despachado',
                'estado': pedido.estadoActual,
                'version': pedido.version
            })
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error al despachar: {str(e)}'}, status=500)
    
@login_required
@role_required(["TrabajadorBodega"])
def actualizar_estado(request, pedido_id):
    """Vista para actualizar el estado de un pedido."""
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if pedido.estado == "pendiente":
        producto = pedido.producto
        if producto.stock >= pedido.cantidad:
            producto.stock -= pedido.cantidad
            producto.save()
            pedido.estado = "despachado"
            pedido.save()
            return JsonResponse({
                "id": pedido.id,
                "estado": pedido.estado,
                "producto": producto.nombre,
                "stock_restante": producto.stock
            })
        else:
            return JsonResponse({
                "error": f"No hay stock suficiente para despachar el pedido. Disponible: {producto.stock}, Solicitado: {pedido.cantidad}"
            }, status=400)

    return JsonResponse({"id": pedido.id, "estado": pedido.estado})

@login_required
@role_required(["Gerente"])
def reporte_productos(request):
    """Vista para generar un reporte de los productos más vendidos en los últimos 3 meses."""
    inicio = time.time()

    hace_tres_meses = timezone.now() - timedelta(days=90)
    productos = (Pedido.objects
                 .filter(fecha_pedido__gte=hace_tres_meses)
                 .values("producto__nombre")
                 .annotate(total_vendido=Sum("cantidad"))
                 .order_by("-total_vendido")[:10])

    fin = time.time()
    latencia = fin - inicio

    return render(request, "pedidos/reporte.html", {
        "productos": productos,
        "latencia": f"{latencia:.2f} segundos"
    })

@login_required
@role_required(["TrabajadorBodega"])
def despachar_multiple(request):
    """Vista para despachar múltiples pedidos."""
    if request.method == 'POST':
        pedidos_ids = request.POST.getlist('pedidos_ids')
        
        if not pedidos_ids:
            messages.warning(request, 'No se seleccionaron pedidos')
            return redirect('lista_pedidos')
        
        despachados = 0
        errores = 0
        
        with transaction.atomic():
            for pedido_id in pedidos_ids:
                try:
                    pedido = Pedido.objects.select_for_update().select_related('producto').get(id=pedido_id)
                    
                    if pedido.estado == 'pendiente' and pedido.producto.stock >= pedido.cantidad:
                        pedido.producto.stock -= pedido.cantidad
                        pedido.estado = 'despachado'
                        
                        pedido.producto.save(update_fields=['stock'])
                        pedido.save(update_fields=['estado'])
                        despachados += 1
                    else:
                        errores += 1
                        
                except Pedido.DoesNotExist:
                    errores += 1
        
        if despachados > 0:
            messages.success(request, f'{despachados} pedidos despachados exitosamente')
        if errores > 0:
            messages.warning(request, f'{errores} pedidos no pudieron ser despachados (ya despachados o sin stock)')
    
    return redirect('lista_pedidos')