import os
import django
import random
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "provesi.settings")
django.setup()

from pedidos.models import Producto, Pedido, EstadosPedido, TipoPedido, CategoriasProducto


# --------- GENERACIÓN DE PRODUCTOS --------- #

def generar_productos():
    productos_base = [
        ("Guantes de nitrilo resistentes a químicos", CategoriasProducto.PROTECCION_MANUAL),
        ("Tapones auditivos de espuma", CategoriasProducto.PROTECCION_AUDITIVA),
        ("Gafas de seguridad antifog", CategoriasProducto.PROTECCION_VISUAL),
        ("Respirador de media cara con filtros", CategoriasProducto.PROTECCION_RESPIRATORIA),
        ("Casco de seguridad dieléctrico", CategoriasProducto.PROTECCION_FACIAL_Y_CABEZA),
        ("Arnés de cuerpo completo certificado", CategoriasProducto.PROTECCION_ALTURAS),
        ("Botas punta de acero Croydon", CategoriasProducto.PROTECCION_PIES),
        ("Kit de primeros auxilios empresarial", CategoriasProducto.PRIMEROS_AUXILIOS),
        ("Señalización de salida de emergencia", CategoriasProducto.SENALIZACION),
        ("Extintor multipropósito 10Lb", CategoriasProducto.ATENCION_DERRAMES),
        ("Overol antifluido industrial", CategoriasProducto.PROTECCION_CORPORAL),
        ("Guantes térmicos resistentes al calor", CategoriasProducto.PROTECCION_MANUAL),
    ]

    productos_creados = []

    for idx, (desc, categoria) in enumerate(productos_base):
        p = Producto(
            SKU=f"PRV-{1000+idx}",
            descripcion=desc,
            referencia=f"REF-{2000+idx}",
            peso=round(random.uniform(0.3, 4.0), 2),
            categoria=categoria
        )
        productos_creados.append(p)

    Producto.objects.bulk_create(productos_creados, ignore_conflicts=True)
    print(f"✅ Se crearon {len(productos_creados)} productos.")


# --------- GENERACIÓN DE PEDIDOS --------- #

def generar_pedidos(n=50):
    productos = list(Producto.objects.all())
    if not productos:
        print("❌ No hay productos. Ejecuta primero la generación de productos.")
        return

    for _ in range(n):
        pedido = Pedido.objects.create(
            estadoActual=random.choice([e.value for e in EstadosPedido]),
            historialEstados=[],
            tipoPedido=random.choice([t.value for t in TipoPedido]),
            bodega=random.choice(["Bodega Norte", "Bodega Occidente", "Bodega Central"]),
            observaciones=random.choice(["", "Prioridad alta", "Cliente solicitó confirmación", "Entregar urgente"]),
        )

        productos_seleccionados = random.sample(productos, random.randint(1, 5))
        pedido.productos.add(*productos_seleccionados)

        # Valor total (sumando un precio simulado según peso para mantener coherencia)
        pedido.valorTotal = round(sum(p.peso * random.randint(5000, 15000) for p in productos_seleccionados), 2)

        # Fecha entrega aleatoria dentro de los próximos 30 días
        pedido.fechaEntrega = timezone.now() + timezone.timedelta(days=random.randint(1, 30))

        # Historial del pedido simulado
        pedido.historialEstados = [
            {"estado": EstadosPedido.COTIZACION.value, "fecha": str(timezone.now())},
            {"estado": pedido.estadoActual, "fecha": str(timezone.now())}
        ]

        pedido.save()

    print(f"✅ Se crearon {n} pedidos.")


# --------- EJECUCIÓN --------- #

if __name__ == "__main__":
    print("🚀 Poblando base de datos...")
    generar_productos()
    generar_pedidos(150)   # Cambia 150 si quieres más volumen
    print("🎉 Finalizado.")
