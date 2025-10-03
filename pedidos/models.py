from django.db import models
from django.utils import timezone


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)  # 👈 NUEVO CAMPO

    def __str__(self):
        return f"{self.nombre} (${self.precio}) - Stock: {self.stock}"


class Pedido(models.Model):
    cliente = models.CharField(max_length=100)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    estado = models.CharField(
        max_length=20,
        choices=[('pendiente', 'Pendiente'), ('despachado', 'Despachado')],
        default='pendiente'
    )

    def __str__(self):
        return f"{self.cliente} - {self.producto.nombre} ({self.cantidad})"
