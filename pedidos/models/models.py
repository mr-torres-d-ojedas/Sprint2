# Models for the pedidos microservice

from enum import Enum
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime
from models.db import PyObjectId
import hashlib
import json


# ---------- ENUMERACIONES ---------- #

class EstadosPedido(str, Enum):
    TRANSITO = "TRÁNSITO"
    ALISTAMIENTO = "ALISTAMIENTO"
    POR_VERIFICAR = "POR VERIFICAR"
    RECHAZADO_X_VERIFICAR = "RECHAZADO X VERIFICAR"
    VERIFICADO = "VERIFICADO"
    EMPACADO_X_DESPACHAR = "EMPACADO X DESPACHAR"
    DESPACHADO = "DESPACHADO"
    DESPACHADO_X_FACTURAR = "DESPACHADO X FACTURAR"
    ENTREGADO = "ENTREGADO"
    DEVUELTO = "DEVUELTO"
    PRODUCCION = "PRODUCCIÓN"
    BORDADO = "BORDADO"
    DROPSHIPPING = "DROPSHIPPING"
    COMPRA = "COMPRA"
    ANULADO = "ANULADO"
    COTIZACION = "COTIZACIÓN"


class TipoPedido(str, Enum):
    DIFERIDO = "DIFERIDO"
    INMEDIATO = "INMEDIATO"


# ---------- MODELOS ---------- #



class Pedido(BaseModel):
    code: str = Field(...)
    estadoActual: EstadosPedido = Field(default=EstadosPedido.COTIZACION)
    historialEstados: List[dict] = Field(default_factory=list)
    tipoPedido: TipoPedido = Field(default=TipoPedido.DIFERIDO)
    bodega: Optional[str] = Field(None)
    productos: List[str] = Field(default_factory=list)  # Lista de IDs de productos
    valorTotal: float = Field(default=0.0)
    observaciones: Optional[str] = Field(None)
    fechaEntrega: Optional[datetime] = Field(None)
    
    # ASR control
    version: int = Field(default=0)
    integrity_hash: Optional[str] = Field(None)
    snapshot: Optional[str] = Field(None)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "code": "PED-2024-001",
                "estadoActual": EstadosPedido.COTIZACION,
                "historialEstados": [],
                "tipoPedido": TipoPedido.DIFERIDO,
                "bodega": "Bodega Central",
                "productos": [],
                "valorTotal": 150000.0,
                "observaciones": "Pedido urgente",
                "fechaEntrega": "2024-12-15T10:00:00",
                "version": 0,
            }
        },
    )
    
    def compute_integrity(self):
        """Calcula el hash de integridad de los campos críticos"""
        critical = {
            "estadoActual": self.estadoActual.value if self.estadoActual else None,
            "valorTotal": str(self.valorTotal) if self.valorTotal is not None else None,
            "fechaEntrega": self.fechaEntrega.isoformat() if self.fechaEntrega else None
        }
        raw = json.dumps(critical, sort_keys=True)
        return hashlib.sha256(raw.encode()).hexdigest(), raw
    
    def seal(self):
        """Sella el pedido con hash de integridad"""
        h, snap = self.compute_integrity()
        self.integrity_hash = h
        self.snapshot = snap


class PedidoOut(Pedido):
    id: PyObjectId = Field(alias="_id", default=None, serialization_alias="id")
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "64b9f1f4f1d2b2a3c4e5f6a7",
                "code": "PED-2024-001",
                "estadoActual": EstadosPedido.COTIZACION,
                "historialEstados": [],
                "tipoPedido": TipoPedido.DIFERIDO,
                "bodega": "Bodega Central",
                "productos": [],
                "valorTotal": 150000.0,
                "observaciones": "Pedido urgente",
                "fechaEntrega": "2024-12-15T10:00:00",
                "version": 0,
            }
        },
    )


class PedidoCollection(BaseModel):
    # A collection of pedidos
    pedidos: List[PedidoOut] = Field(...)

