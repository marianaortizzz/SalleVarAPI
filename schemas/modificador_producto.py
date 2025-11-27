from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class OpcionModificadorBase(BaseModel):
    nombre: str
    precio: float
    descripcion: Optional[str] = None
    disponible: bool

    class Config:
        json_schema = {
            "example": {
                "nombre": "Grande",
                "precio": 2.0,
                "disponible": True,
                "descripcion": "Tamaño grande del producto"
            }
        }
        from_attributes = True


class OpcionModificadorCreate(OpcionModificadorBase):
    pass

class OpcionModificadorUpdate(BaseModel):
    nombre: Optional[str] = None
    precio: Optional[float] = None
    descripcion: Optional[str] = None
    disponible: Optional[bool] = None

class OpcionModificador(OpcionModificadorBase):
    id: int
    id_producto: int

    model_config= ConfigDict(from_attributes=True)



class ModificadorProductoBase(BaseModel):
    nombre_modificador: str
    num_max_selec: int

    class Config:
        json_schema = {
            "example": {
                "nombre_modificador": "Tamaño",
                "num_max_selec": 1
            }
        }
        from_attributes = True

class ModificadorProductoCreate(ModificadorProductoBase):
    pass

class ModificadorProductoUpdate(BaseModel):
    nombre_modificador: Optional[str] = None
    num_max_selec: Optional[int] = None
    opciones: Optional[List[OpcionModificadorUpdate]] = None

class ModificadorProducto(ModificadorProductoBase):
    id: int
    id_producto: int
    opciones: List[OpcionModificador] = []

    model_config = ConfigDict(from_attributes=True)

