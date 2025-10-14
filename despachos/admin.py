from django.contrib import admin
from .models import Despacho


@admin.register(Despacho)
class DespachoAdmin(admin.ModelAdmin):
        list_display = ("id", "pedido", "cliente", "producto", "cantidad", "completado_en")
        list_filter = ("completado_en",)
        search_fields = ("pedido__cliente", "pedido__producto__nombre")
        autocomplete_fields = ("pedido",)
        date_hierarchy = "completado_en"
        list_select_related = ("pedido", "pedido__producto")
        list_per_page = 25

        def cliente(self, obj):
                return obj.cliente

        def producto(self, obj):
                return obj.producto

        def cantidad(self, obj):
                return obj.cantidad