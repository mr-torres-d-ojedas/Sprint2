import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "provesi.settings")
django.setup()

from pedidos.models import Pedido

def main():
    count = 0
    for p in Pedido.objects.all():
        if not p.integrity_hash:
            p.seal()
            p.save(update_fields=["integrity_hash", "snapshot"])
            count += 1
    print(f"Sellados {count} pedidos.")

if __name__ == "__main__":
    main()