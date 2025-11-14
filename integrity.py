from django.core.management.base import BaseCommand
from pedidos.models import Pedido

class Command(BaseCommand):
    help = "Inicializa integrity_hash y snapshot en pedidos existentes."

    def handle(self, *args, **options):
        count = 0
        for p in Pedido.objects.all():
            if not p.integrity_hash:
                p.seal()
                p.save(update_fields=["integrity_hash", "snapshot"])
                count += 1
        self.stdout.write(self.style.SUCCESS(f"Sellados {count} pedidos."))