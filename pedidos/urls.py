from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_pedidos, name='lista_pedidos'),
    path('<int:pedido_id>/despachar/', views.despachar_pedido, name='despachar_pedido'),
    path('reporte/', views.reporte_productos, name='reporte'),
     path('', views.index, name='pedidos_index'),
]





