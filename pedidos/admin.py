from django.contrib import admin
from .models import Producto, Pedido

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("SKU", "descripcion", "categoria", "peso")
    search_fields = ("SKU", "descripcion", "categoria")


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "estadoActual", "tipoPedido", "valorTotal", "fechaEntrega")
    list_filter = ("estadoActual", "tipoPedido")
    search_fields = ("id",)
    filter_horizontal = ("productos",)
