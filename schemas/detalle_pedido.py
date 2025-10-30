from pydantic import BaseModel, Field
from decimal import Decimal

class DetallePedido(BaseModel):
    id_pedido: int = Field(ge=1)
    id_producto: int = Field(ge=1)
    cantidad: int = Field(ge=1)
    precio_unitario: Decimal = Field(ge=0, decimal_places=2)

    class Config:
        json_schema = {
            "example": {
                "id_detalle_pedido": 1,
                "id_pedido": 1,
                "id_producto": 1,
                "cantidad": 2,
                "precio_unitario": 75.25
            }
        }
