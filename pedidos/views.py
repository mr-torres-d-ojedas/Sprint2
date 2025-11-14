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
import hashlib, json, time

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
@role_required(["TrabajadorBodega"])
def despachar_pedido(request, pedido_id):
    start = time.time()  # medir latencia detección

    role = getRole(request)
    if role == "TrabajadorBodega":
        print(f"APROBADO: rol={role} puede despachar pedido {pedido_id}")
    else:
        print(f"DENEGADO: rol={role} no puede despachar pedido {pedido_id}")
        return JsonResponse({'success': False, 'message': 'No tiene permisos'}, status=403)

    client_version = request.headers.get('X-Pedido-Version') or request.POST.get('version')
    try:
        client_version = int(client_version) if client_version is not None else None
    except ValueError:
        client_version = None

    try:
        with transaction.atomic():
            pedido = get_object_or_404(Pedido.objects.select_for_update(), id=pedido_id)

            # Verificar integridad previa
            expected_hash, raw_snapshot = pedido.compute_integrity()
            if pedido.integrity_hash and pedido.integrity_hash != expected_hash:
                # Modificación externa detectada → revertir a snapshot
                print(f"ALERTA ATAQUE: integridad violada en Pedido {pedido.id}. Revocando cambios.")
                # Revocar: restaurar snapshot (estado aprobado previo)
                snap = json.loads(pedido.snapshot) if pedido.snapshot else {}
                pedido.estadoActual = snap.get("estadoActual")
                pedido.valorTotal = snap.get("valorTotal")
                # No avanzar estado; re-sellar
                pedido.seal()
                pedido.save(update_fields=["estadoActual", "valorTotal", "integrity_hash", "snapshot", "updated_at"])
                elapsed = (time.time() - start)
                return JsonResponse({
                    "success": False,
                    "revocado": True,
                    "tiempo_revocacion_s": f"{elapsed:.3f}",
                    "message": "Intento no autorizado detectado y revertido."
                }, status=409)

            # Concurrencia versión
            if client_version is not None and pedido.version != client_version:
                print(f"CONFLICTO VERSION Pedido {pedido.id}: cliente={client_version} servidor={pedido.version}")
                elapsed = (time.time() - start)
                return JsonResponse({
                    'success': False,
                    'message': 'Conflicto de versión. Recargue.',
                    'tiempo_revocacion_s': f"{elapsed:.3f}"
                }, status=409)

            if pedido.estadoActual == EstadosPedido.DESPACHADO:
                return JsonResponse({'success': False, 'message': 'Ya despachado'}, status=400)

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
            # Sellar nuevo estado
            pedido.seal()
            pedido.save(update_fields=['estadoActual','historialEstados','version','integrity_hash','snapshot','updated_at'])

            elapsed = (time.time() - start)
            return JsonResponse({
                'success': True,
                'message': f'Pedido #{pedido.id} despachado',
                'estado': pedido.estadoActual,
                'version': pedido.version,
                'tiempo_proceso_s': f"{elapsed:.3f}"
            })
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error: {str(e)}'}, status=500)
    
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