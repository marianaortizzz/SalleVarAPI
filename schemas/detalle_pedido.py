from pydantic import BaseModel, Field
from typing import Optional

class DetallePedido(BaseModel):
    id_detalle_pedido: int = Field(..., description="Identificador único del detalle del pedido")
    id_pedido: int = Field(..., description="Identificador del pedido asociado")
    id_producto: int = Field(..., description="Identificador del producto asociado")
    cantidad: int = Field(..., description="Cantidad de productos en el detalle del pedido")
    precio_unitario: Optional[float] = Field(None, description="Precio unitario del producto")
    rating: Optional[float] = Field(None, description="Rating del producto en el pedido")

    class Config:
        from_attributes = True
        json_schema = {
            "example": {
                "id_detalle_pedido": 1,
                "id_pedido": 10,
                "id_producto": 5,
                "cantidad": 2,
                "precio_unitario": 15.50,
                "rating": 4.5
            }
        }
