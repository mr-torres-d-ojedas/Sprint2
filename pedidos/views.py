from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.db import transaction
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from .models import Pedido, Producto
from django.contrib.auth.decorators import login_required


import time

def index(request):
    return render(request, "pedidos/index.html")

def lista_pedidos(request):
    pedidos = Pedido.objects.prefetch_related('productos').all()
    return render(request, "pedidos/lista.html", {"pedidos": pedidos})


@csrf_exempt  # Solo para testing, considera agregar CSRF en producción
@require_POST
def despachar_pedido(request, pedido_id):
    """Vista para despachar un pedido específico."""
    try:
        with transaction.atomic():
            # Obtener pedido con select_for_update para evitar race conditions
            pedido = get_object_or_404(
                Pedido.objects.select_for_update().select_related('producto'), 
                id=pedido_id
            )
            
            # Verificar si ya está despachado
            if pedido.estado == 'despachado':
                return JsonResponse({
                    'success': False, 
                    'message': 'El pedido ya está despachado'
                }, status=400)
            
            # Verificar stock disponible
            producto = pedido.producto
            if producto.stock < pedido.cantidad:
                return JsonResponse({
                    'success': False,
                    'message': f'Stock insuficiente. Disponible: {producto.stock}, Solicitado: {pedido.cantidad}'
                }, status=400)
            
            # Actualizar stock y estado del pedido
            producto.stock -= pedido.cantidad
            pedido.estado = 'despachado'
            
            # Guardar cambios
            producto.save(update_fields=['stock'])
            pedido.save(update_fields=['estado'])
            
            # Respuesta exitosa
            return JsonResponse({
                'success': True,
                'message': f'Pedido #{pedido.id} despachado exitosamente',
                'nuevo_stock': producto.stock,
                'estado': pedido.estado
            })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al despachar pedido: {str(e)}'
        }, status=500)

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

def reporte_productos(request):
    """Vista para generar un reporte de los productos más vendidos en los últimos 3 meses."""
    inicio = time.time()

    hace_tres_meses = timezone.now() - timedelta(days=90)
    productos = (Pedido.objects
                 .filter(fecha_pedido__gte=hace_tres_meses)  # Cambiado a fecha_pedido
                 .values("producto__nombre")
                 .annotate(total_vendido=Sum("cantidad"))
                 .order_by("-total_vendido")[:10])

    fin = time.time()
    latencia = fin - inicio

    return render(request, "pedidos/reporte.html", {
        "productos": productos,
        "latencia": f"{latencia:.2f} segundos"
    })

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
