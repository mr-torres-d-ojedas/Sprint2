from django.db import models
from django.utils import timezone


class Despacho(models.Model):
        pedido = models.OneToOneField(
                "pedidos.Pedido",
                on_delete=models.CASCADE,
                related_name="registro_despacho",
                verbose_name="Pedido",
        )
        completado_en = models.DateTimeField("Completado en", default=timezone.now)
        creado_en = models.DateTimeField("Creado en", auto_now_add=True)

        class Meta:
                verbose_name = "Despacho"
                verbose_name_plural = "Despachos"
                ordering = ["-completado_en"]
                indexes = [
                        models.Index(fields=["completado_en"]),
                        models.Index(fields=["pedido", "completado_en"]),
                ]

        def __str__(self):
                return f"Despacho #{self.pk} - Pedido #{self.pedido_id}"

        @property
        def cliente(self):
                return self.pedido.cliente

        @property
        def producto(self):
                return self.pedido.producto

        @property
        def cantidad(self):
                return self.pedido.cantidad