import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "provesi.settings")
django.setup()

from pedidos.models import Pedido

p = Pedido.objects.get(id=2)
p.estadoActual = 'VERIFICADO'  # cambio malicioso
p.save(update_fields=['estadoActual'])
print("Estado modificado externamente (simulación ataque).")