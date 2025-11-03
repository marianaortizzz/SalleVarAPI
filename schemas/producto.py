from pydantic import BaseModel, Field   

class Producto(BaseModel):
    id_producto: int = Field(..., description="Identificador único del producto")
    nombre: str | None = Field(..., description="Nombre del producto")
    precio: float | None = Field(..., description="Precio del producto")
    descripcion: str | None = Field(..., description="Descripción del producto")
    imagen: str | None = Field(..., description="URL de la imagen del producto")
    categoria: str | None = Field(..., description="Categoría del producto")
    disponible: bool = Field(..., description="Disponibilidad del producto")
    id_negocio: int | None = Field(..., description="Identificador del negocio al que pertenece el producto")

    class Config:
        orm_mode = True
        json_schema = {
            "example": {
                "id_producto": 1,
                "nombre": "Producto Ejemplo",
                "precio": 19.99,
                "descripcion": "Descripción del producto ejemplo",
                "imagen": "imagen.jpg",
                "categoria": "Categoría Ejemplo",
                "disponible": True,
                "id_negocio": 2
            }
        }