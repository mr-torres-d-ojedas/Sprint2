from django.contrib import admin
from .models import Producto, Pedido


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
	list_display = ("id", "nombre", "precio", "stock")
	list_editable = ("stock",)
	search_fields = ("nombre",)
	list_per_page = 25


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
	list_display = ("id", "cliente", "producto", "cantidad", "estado", "fecha_pedido")
	list_filter = ("estado", "fecha_pedido")
	search_fields = ("cliente", "producto__nombre")
	autocomplete_fields = ("producto",)
	date_hierarchy = "fecha_pedido"
	list_per_page = 25
