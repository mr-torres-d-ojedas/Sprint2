from django.urls import path

from . import views

app_name = "despachos"

urlpatterns = [
        path("reporte/", views.reporte_productos_despachados, name="reporte"),
]