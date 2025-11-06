from django.db import models
from django.utils import timezone

# ---------- ENUMERACIONES ---------- #

class CategoriasProducto(models.TextChoices):
    PROTECCION_MANUAL = "PROTECCIÓN MANUAL", "Protección Manual"
    PROTECCION_AUDITIVA = "PROTECCIÓN AUDITIVA", "Protección Auditiva"
    PROTECCION_VISUAL = "PROTECCIÓN VISUAL", "Protección Visual"
    PROTECCION_RESPIRATORIA = "PROTECCIÓN RESPIRATORIA", "Protección Respiratoria"
    PROTECCION_FACIAL_Y_CABEZA = "PROTECCIÓN FACIAL Y CABEZA", "Protección Facial y Cabeza"
    PROTECCION_CORPORAL = "PROTECCIÓN CORPORAL", "Protección Corporal"
    SENALIZACION = "SEÑALIZACIÓN", "Señalización"
    PROTECCION_ALTURAS = "PROTECCIÓN ALTURAS", "Protección Alturas"
    PROTECCION_PIES = "PROTECCIÓN PIES", "Protección Pies"
    PRIMEROS_AUXILIOS = "ATENCIÓN PRIMEROS AUXILIOS", "Atención Primeros Auxilios"
    ESPACIOS_CONFINADOS = "PROTECCIÓN ESPACIOS CONFINADOS", "Protección Espacios Confinados"
    ATENCION_DERRAMES = "MATERIAL ATENCIÓN DERRAMES", "Material Atención Derrames"
    HERRAMIENTAS_EQUIPOS = "HERRAMIENTAS Y EQUIPOS", "Herramientas y Equipos"
    OTROS = "OTROS", "Otros"
    TECNOLOGIA = "TECNOLOGÍA", "Tecnología"


class EstadosPedido(models.TextChoices):
    TRANSITO = "TRÁNSITO", "Tránsito"
    ALISTAMIENTO = "ALISTAMIENTO", "Alistamiento"
    POR_VERIFICAR = "POR VERIFICAR", "Por Verificar"
    RECHAZADO_X_VERIFICAR = "RECHAZADO X VERIFICAR", "Rechazado por Verificar"
    VERIFICADO = "VERIFICADO", "Verificado"
    EMPACADO_X_DESPACHAR = "EMPACADO X DESPACHAR", "Empacado por Despachar"
    DESPACHADO = "DESPACHADO", "Despachado"
    DESPACHADO_X_FACTURAR = "DESPACHADO X FACTURAR", "Despachado por Facturar"
    ENTREGADO = "ENTREGADO", "Entregado"
    DEVUELTO = "DEVUELTO", "Devuelto"
    PRODUCCION = "PRODUCCIÓN", "Producción"
    BORDADO = "BORDADO", "Bordado"
    DROPSHIPPING = "DROPSHIPPING", "Dropshipping"
    COMPRA = "COMPRA", "Compra"
    ANULADO = "ANULADO", "Anulado"
    COTIZACION = "COTIZACIÓN", "Cotización"


class TipoPedido(models.TextChoices):
    DIFERIDO = "DIFERIDO", "Diferido"
    INMEDIATO = "INMEDIATO", "Inmediato"


# ---------- MODELOS ---------- #

class Producto(models.Model):
    SKU = models.CharField(max_length=100, null=True, blank=True)
    descripcion = models.CharField(max_length=250)
    referencia = models.CharField(max_length=150, blank=True, null=True)
    peso = models.FloatField(default=0.0)
    categoria = models.CharField(
        max_length=50,
        choices=CategoriasProducto.choices,
        default=CategoriasProducto.OTROS
    )
    def __str__(self):
        return f"{self.SKU} - {self.descripcion}"


class Pedido(models.Model):
    estadoActual = models.CharField(
        max_length=40,
        choices=EstadosPedido.choices,
        default=EstadosPedido.COTIZACION
    )
    historialEstados = models.JSONField(default=list)
    tipoPedido = models.CharField(max_length=20, choices=TipoPedido.choices, default=TipoPedido.DIFERIDO)

    bodega = models.CharField(max_length=100, blank=True, null=True)
    productos = models.ManyToManyField(Producto)

    valorTotal = models.FloatField(default=0)
    observaciones = models.TextField(blank=True, null=True)
    fechaEntrega = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.estadoActual}"
