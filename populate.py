import os
import django
import random
from decimal import Decimal
from django.utils import timezone
from django.db import transaction

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "provesi.settings")
django.setup()

from pedidos.models import Producto, Pedido, EstadosPedido, TipoPedido, CategoriasProducto


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


def generar_pedidos(n=50):
    productos = list(Producto.objects.all())
    if not productos:
        print("❌ No hay productos. Ejecuta primero generar_productos().")
        return

    with transaction.atomic():
        for _ in range(n):
            productos_seleccionados = random.sample(productos, random.randint(1, 5))

            # Calcular valorTotal (precio simulado = peso * factor aleatorio)
            total = Decimal("0")
            for prod in productos_seleccionados:
                factor = Decimal(random.randint(5000, 15000))
                total += Decimal(str(prod.peso)) * factor

            # Fecha de entrega
            fecha_entrega = timezone.now() + timezone.timedelta(days=random.randint(1, 30))

            estado = random.choice([e.value for e in EstadosPedido])
            tipo = random.choice([t.value for t in TipoPedido])
            bodega = random.choice(["Bodega Norte", "Bodega Occidente", "Bodega Central"])
            obs = random.choice(["", "Prioridad alta", "Cliente solicitó confirmación", "Entregar urgente"])

            historial = [
                {"estado": EstadosPedido.COTIZACION.value, "fecha": str(timezone.now())},
                {"estado": estado, "fecha": str(timezone.now())}
            ]

            # Crear pedido con campos críticos ya definidos (sellado interno OK)
            pedido = Pedido.objects.create(
                estadoActual=estado,
                historialEstados=historial,
                tipoPedido=tipo,
                bodega=bodega,
                observaciones=obs,
                valorTotal=total,
                fechaEntrega=fecha_entrega,
            )

            # Añadir productos (no afecta integridad crítica)
            pedido.productos.add(*productos_seleccionados)

            # Reseal opcional por si el save inicial no tomó algún valor tardío (seguro)
            pedido.seal()
            pedido.save(update_fields=["integrity_hash", "snapshot"])

    print(f"✅ Se crearon {n} pedidos.")


if __name__ == "__main__":
    print("🚀 Poblando base de datos...")
    generar_productos()
    generar_pedidos(150)
    print("🎉 Finalizado.")