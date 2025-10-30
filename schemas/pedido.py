from pydantic import BaseModel, Field
from typing import Literal
from datetime import date
from decimal import Decimal

class Pedido(BaseModel):
    fecha_pedido: date
    status: Literal["Pendiente", "En_proceso", "Completado", "Cancelado"]
    id_cliente: int = Field(ge=1)
    id_negocio: int = Field(ge=1)
    monto_total: Decimal = Field(ge=0, decimal_places=2)
    status_pago: Literal["Pendiente", "Pagado", "Rechazado"]
    rating_pedido: Decimal | None = Field(default=None, ge=0, le=5, decimal_places=1)

    class Config:
        json_schema = {
            "example": {
                "campo": 1,
                "fecha_pedido": "2025-10-29",
                "status": "Pendiente",
                "id_cliente": 1,
                "id_negocio": 1,
                "monto_total": 150.50,
                "status_pago": "Pendiente",
                "rating_pedido": 4.5
            }
        }
