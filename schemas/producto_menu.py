from pydantic import BaseModel
from typing import List
from SalleVarAPI.schemas.modificador_producto import ModificadorProducto

class ProductoMenu(BaseModel):
    id_producto: int
    nombre: str
    precio: float
    descripcion: str
    imagen: str
    categoria: str
    disponible: bool
    id_negocio: int
    modificadores: List[ModificadorProducto]

    class Config:
        json_schema = {
            "example": {
                "id_producto": "1",
                "nombre": "Hamburguesa",
                "precio": 8.99,
                "descripcion": "Deliciosa hamburguesa con queso",
                "imagen": "hamburguesa.jpg",
                "categoria": "Comida Rápida",
                "disponible": True,
                "id_negocio": 101,
                "modificadores": [ ]
            }
        }