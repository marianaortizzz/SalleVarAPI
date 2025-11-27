from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import time

class Negocio(BaseModel):
    id_negocio: int | None = Field(default=None)
    nombre: str = Field(..., description="Nombre del negocio")
    contrasena: Optional[str] = Field(None, description="Contraseña del negocio")
    rating: Optional[float] = Field(None, description="Rating del negocio")
    rango_precios: Optional[str] = Field(None, description="Rango de precios del negocio")
    ubicacion: Optional[str] = Field(None, description="Ubicación del negocio")
    nombre_responsable: Optional[str] = Field(None, description="Nombre del responsable del negocio")
    telefono: Optional[str] = Field(None, description="Teléfono del negocio")
    categorias: Optional[str] = Field(None, description="Categorías del negocio")
    imagen: Optional[str] = Field(None, description="URL de la imagen del negocio")
    horario_apertura: Optional[time] = Field(None, description="Horario de apertura del negocio")
    horario_cierre: Optional[time] = Field(None, description="Horario de cierre del negocio")
    activo: Optional[bool] = Field(None, description="Estado activo del negocio")

    class Config:
        from_attributes = True
        json_schema = {
            "example": {
                "id_negocio": 1,
                "nombre": "Negocio Ejemplo",
                "contrasena": "securepassword",
                "rating": 4.5,
                "rango_precios": "50-100",
                "ubicacion": "Calle Falsa 123",
                "nombre_responsable": "Juan Pérez",
                "telefono": "123456789",
                "categorias": "Comida, Bebidas",
                "imagen": "imagen_negocio.jpg",
                "horario_apertura": "09:00:00",
                "horario_cierre": "22:00:00",
                "activo": True
            }
        }   
        