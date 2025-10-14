import os
import django
from datetime import timedelta
from random import randint

from django.utils import timezone
from django.db import transaction

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "provesi.settings")
django.setup()

from pedidos.models import Pedido
from despachos.models import Despacho


BATCH_SIZE = 500


def completado_en_para(pedido):
    """
    Fecha de completado aleatoria entre fecha_pedido y ahora.
    Asegura que nunca sea en el futuro.
    """
    now = timezone.now()
    start = pedido.fecha_pedido or (now - timedelta(days=120))
    if start > now:
        start = now - timedelta(minutes=1)
    total_seconds = int((now - start).total_seconds())
    delta = timedelta(seconds=randint(0, max(total_seconds, 0)))
    return start + delta


def main():
    print("== Poblando tabla 'despachos' a partir de pedidos despachados ==")

    qs = (
        Pedido.objects
        .filter(estado="despachado", registro_despacho__isnull=True)
        .only("id", "fecha_pedido")
        .order_by("id")
    )

    total = qs.count()
    if total == 0:
        print("No hay pedidos 'despachado' pendientes por registrar en despachos.")
        return

    print(f"Pedidos candidatos: {total}")
    creados = 0
    buffer = []

    with transaction.atomic():
        for idx, pedido in enumerate(qs.iterator(chunk_size=BATCH_SIZE), start=1):
            buffer.append(
                Despacho(
                    pedido=pedido,
                    completado_en=completado_en_para(pedido),
                )
            )

            if len(buffer) >= BATCH_SIZE:
                Despacho.objects.bulk_create(buffer, ignore_conflicts=True)
                creados += len(buffer)
                buffer.clear()
                if creados % 1000 == 0:
                    print(f"Progreso: {creados}/{total} registros creados...")

        if buffer:
            Despacho.objects.bulk_create(buffer, ignore_conflicts=True)
            creados += len(buffer)
            buffer.clear()

    print(f"Listo. Despachos creados: {creados} de {total} pedidos candidatos.")


if __name__ == "__main__":
    main()