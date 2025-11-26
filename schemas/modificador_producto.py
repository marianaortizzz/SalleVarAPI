from pydantic import BaseModel
from typing import List, Optional

class OpcionModificador(BaseModel):
    id_opcion: int
    nombre: str
    precio_adicional: float
    descripcion: Optional[str] = None
    disponible: bool
    id_modificador: int

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
        orm_mode = True
        from_attributes = True

class ModificadorProducto(BaseModel):
    id_modificador: int
    nombre_modificador: str
    num_max_selec: int
    opciones: List[OpcionModificador]
    id_producto: int

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
        orm_mode = True
        from_attributes = True