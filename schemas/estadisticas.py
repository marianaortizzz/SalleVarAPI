from pydantic import BaseModel, Field
from datetime import date

class Estadistica(BaseModel):
    id_estadistica: int = Field(ge=1, description="Identificador único de la estadística")
    fecha_inicio: date = Field(description="Fecha de inicio del periodo de la estadística")
    monto_total: float = Field(min_value=0, description="Monto total generado en el periodo")
    rating_promedio: float = Field(ge=0, le=5, description="Rating promedio de los productos vendidos")
    producto_mas_vendido: str = Field(min_length=1, description="Nombre del producto más vendido")
    numero_ventas: int = Field(ge=0, description="Número total de ventas en el periodo")
    id_restaurante: int = Field(ge=1, description="Identificador del restaurante asociado")

    class Config:
        from_attributes = True
        json_schema = {
            "example": {
                "id_estadistica": 1,
                "fecha_inicio": "2025-01-01",
                "monto_total": 15000.75,
                "rating_promedio": 4.5,
                "producto_mas_vendido": "3,9",
                "numero_ventas": 120, 
                "id_restaurante": 2
            }
        }