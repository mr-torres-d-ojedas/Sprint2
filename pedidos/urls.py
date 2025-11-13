from django.urls import path
from . import views
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from django.contrib import admin


urlpatterns = [
    path('', views.lista_pedidos, name='lista_pedidos'),
    path('despachar/<int:pedido_id>/', views.despachar_pedido, name='despachar_pedido'),
    path('reporte/', views.reporte_productos, name='reporte_productos'),
    path('actualizar/<int:pedido_id>/', views.actualizar_estado, name='actualizar_estado'),
    path('despachar-multiple/', views.despachar_multiple, name='despachar_multiple'),
]