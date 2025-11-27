from decimal import Decimal
from pydantic import BaseModel, Field
from typing import Optional
from schemas.producto_pedido import ProductoPedido

class DetallePedidoCreate(BaseModel):
    id_producto: int
    cantidad: int
    precio_unitario: Decimal = Field(..., description="Precio del producto al momento del pedido")
    rating: Optional[int] = Field(None, description="Rating del producto en el pedido")
    opciones: Optional[str] = Field(None, description="Opciones o modificaciones aplicadas al producto en el pedido")
    comentarios: Optional[str] = Field(None, description="Comentarios adicionales para el producto en el pedido")
    total_producto: Optional[Decimal] = Field(None, description="Total del producto en el pedido")
    

class DetallePedido(DetallePedidoCreate):
    id_detalle_pedido: int
    id_pedido: int

    class Config:
        orm_mode = True