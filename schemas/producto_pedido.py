from pydantic import BaseModel
from typing import List

class ProductoPedido(BaseModel):
    id_producto: int
    nombre: str
    precio: float
    descripcion: str
    cantidad: int
    opciones_seleccionadas: List[str]
    comentarios_extra: str
    total_producto:float


    class Config:
        json_schema = {
            "example": {
                "id_producto": 1,
                "nombre": "Hamburguesa",
                "precio": 8.99,
                "descripcion": "Deliciosa hamburguesa con queso",
                "cantidad": 2,
                "opciones_seleccionadas": ["Queso extra", "Sin cebolla"],
                "comentarios_extra": "Por favor, que esté bien cocida",
                "total_producto":17.98
            }
        }