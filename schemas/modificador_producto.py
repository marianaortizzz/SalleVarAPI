from pydantic import BaseModel
from typing import List, Optional

class OpcionModificador(BaseModel):
    id_opcion: str
    nombre: str
    precio_adicional: float
    disponible: bool
    id_producto: str

    class Config:
        json_schema = {
            "example": {
                "id_opcion": "1",
                "nombre": "Grande",
                "precio_adicional": 2.0,
                "disponible": True,
                "id_producto": "101"
            }
        }

class ModificadorProducto(BaseModel):
    id_modificador: str
    nombre_modificador: str
    num_max_selec: int
    opciones: List[OpcionModificador]

    class Config:
        json_schema = {
            "example": {
                "id_modificador": "1",
                "nombre_modificador": "Tamaño",
                "num_max_selec": 1,
                "opciones": [
                    {
                        "id_opcion": "1",
                        "nombre": "Pequeño",
                        "precio_adicional": 0.0,
                        "disponible": True,
                        "id_producto": "101"
                    },
                    {
                        "id_opcion": "2",
                        "nombre": "Mediano",
                        "precio_adicional": 1.0,
                        "disponible": True,
                        "id_producto": "101"
                    }
                ]
            }
        }