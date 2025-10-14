from datetime import timedelta

from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone
from django.db.utils import OperationalError, ProgrammingError  # <- añadido

from .models import Despacho


def reporte_productos_despachados(request):
        limite = timezone.now() - timedelta(days=90)
        try:
                productos = (
                        Despacho.objects.filter(completado_en__gte=limite)
                        .values("pedido__producto__id", "pedido__producto__nombre")
                        .annotate(total_cantidad=Sum("pedido__cantidad"))
                        .order_by("-total_cantidad")
                )
        except (OperationalError, ProgrammingError):
                productos = []

        contexto = {"productos": productos, "fecha_inicio": limite}
        return render(request, "despachos/reporte.html", contexto)