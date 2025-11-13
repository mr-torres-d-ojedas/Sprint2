from django.urls import path
from . import views
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.lista_pedidos, name='lista_pedidos'),
    path('<int:pedido_id>/despachar/', views.despachar_pedido, name='despachar_pedido'),
    path('reporte/', views.reporte_productos, name='reporte'),
    path(r'', include('django.contrib.auth.urls')),
    path(r'', include('social_django.urls')),

]
