from pydantic import BaseModel
from typing import List
from SalleVarAPI.schemas.modificador_producto import ModificadorProducto

class ProductoMenu(BaseModel):
    id_producto: str
    nombre: str
    precio: float
    descripcion: str
    imagen: str
    categoria: str
    disponible: bool
    id_negocio: str
    modificadores: List[ModificadorProducto]