from pydantic import BaseModel, Field
from typing import Literal
from datetime import date
from decimal import Decimal
from typing import List, Optional
from schemas.cliente import Cliente
from schemas.producto_pedido import ProductoPedido
from schemas.repartidor import Repartidor
from schemas.detalle_pedido import DetallePedidoCreate, DetallePedido, DetallePedidoResponse
from pydantic import ConfigDict

class PedidoBase(BaseModel):
    fecha_pedido: date
    subtotal: Decimal = Field(..., decimal_places=2)
    costo_envio: Decimal = Field(..., decimal_places=2)
    costo_servicio: Decimal = Field(..., decimal_places=2)
    monto_total: Decimal = Field(..., decimal_places=2)
    status_general: Literal['Pendiente', 'En_proceso', 'Completado', 'Cancelado']
    status_rest: Literal['Pendiente', 'Activo', 'Entregado']
    status_rep: Literal['Activo', 'Pendiente', 'Entregado']
    status_pago: Literal['Pendiente', 'Pagado', 'Rechazado']
    codigo_rest: str
    codigo_rep: str
    para_llevar: bool
    delivery: bool
    comentarios: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


class PedidoCreate(PedidoBase):
    id_cliente: int
    id_negocio: int
    detalles: List[DetallePedidoCreate]
    

class Pedido(PedidoBase):
    id_pedido: int
    id_cliente: int
    id_negocio: int
    id_repartidor: Optional[int] = None
    
    rating_pedido: Optional[Decimal] = Field(None, decimal_places=1)
    rating_rep: Optional[Decimal] = Field(None, decimal_places=1)
    
    detalles: List[DetallePedidoResponse] = []


class PedidoUpdate(BaseModel):
    fecha_pedido: Optional[date] = None
    status_general: Optional[Literal['Pendiente', 'En_proceso', 'Completado', 'Cancelado']] = None
    status_rep: Optional[Literal['Asignado', 'En_camino', 'Entregado']] = None
    status_rest: Optional[Literal['Pendiente', 'Preparando', 'Listo']] = None
    id_repartidor: Optional[int] = None
    rating_pedido: Optional[Decimal] = Field(None, decimal_places=1)
    rating_rep: Optional[Decimal] = Field(None, decimal_places=1)
    comentarios: Optional[str] = None
    
    # Nota: Los campos de Detalle (productos, subtotales) 
    # generalmente se actualizan mediante endpoints dedicados o se recrean completamente.