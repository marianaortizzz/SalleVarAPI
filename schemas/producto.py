from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

from schemas.modificador_producto import ModificadorProducto   
from schemas.modificador_producto import ModificadorProductoCreate
    
class ProductoBase(BaseModel):
    nombre: str = Field(..., description="Nombre del producto")
    precio: float = Field(..., description="Precio del producto")
    descripcion: str = Field(..., description="Descripción del producto")
    imagen: str = Field(..., description="URL de la imagen del producto")
    categoria: str = Field(..., description="Categoría del producto")
    disponible: bool = Field(True, description="Disponibilidad del producto") # Con valor por defecto

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "nombre": "Producto Ejemplo",
                "precio": 19.99,
                "descripcion": "Descripción del producto ejemplo",
                "imagen": "imagen.jpg",
                "categoria": "Categoría Ejemplo",
                "disponible": True
            }
        }
    )

class ProductoCreate(ProductoBase):
    modificadores: Optional[List[ModificadorProductoCreate]] = Field(None, description="Lista de modificadores a aplicar al producto.")

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, description="Nombre del producto")
    precio: Optional[float] = Field(None, description="Precio del producto")
    descripcion: Optional[str] = Field(None, description="Descripción del producto")
    imagen: Optional[str] = Field(None, description="URL de la imagen del producto")
    categoria: Optional[str] = Field(None, description="Categoría del producto")
    disponible: Optional[bool] = Field(None, description="Disponibilidad del producto")
    modificadores: Optional[List[ModificadorProductoCreate]] = None 

class Producto(ProductoBase):
    id_producto: int = Field(..., description="Identificador único del producto")
    id_negocio: int = Field(..., description="Identificador del negocio asociado al producto")
    modificadores: Optional[List[ModificadorProducto]] = Field(None, description="Lista de modificadores asociados al producto.") 

    model_config = ConfigDict(
        from_attributes=True
    )



class ProductoPedido(ProductoBase):
    id_producto: int = Field(..., description="Identificador único del producto")
    cantidad: int = Field(..., description="Cantidad del producto en el pedido")
    total_producto: float = Field(..., description="Total del producto en el pedido")
    opciones_seleccionadas: List[str] = Field(..., description="Opciones seleccionadas para el producto")
    comentarios_extra: str = Field(..., description="Comentarios extra para el producto")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id_producto": 1,
                "nombre": "Producto Ejemplo",
                "precio": 19.99,
                "descripcion": "Descripción del producto ejemplo",
                "cantidad": 2,
                "total_producto": 39.98,
                "opciones_seleccionadas": ["Opción 1", "Opción 2"],
                "comentarios_extra": "Sin cebolla",
                "imagen": "imagen.jpg",
                "categoria": "Categoría Ejemplo",
                "disponible": True
            }
        }
    )