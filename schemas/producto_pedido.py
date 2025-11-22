from pydantic import BaseModel
from typing import List

class ProductoPedido(BaseModel):
    id_producto: str
    nombre: str
    precio: float
    descripcion: str
    cantidad: int
    opciones_seleccionadas: List[str]
    comentarios_extra: str