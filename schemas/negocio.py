from pydantic import BaseModel, Field
from typing import Literal
from datetime import time

class Negocio(BaseModel):
    nombre: str = Field(min_length=1, max_length=255)
    categoria: str = Field(min_length=1, max_length=255) 
    rating: float = Field(ge=0, le=5)  # rating 0 a 5
    rango_precios: Literal["0-50", "50-100", "100-150", "150-200", "+200"]
    ubicacion: str = Field(min_length=1, max_length=255)
    nombre_responsable: str = Field(min_length=1, max_length=255)
    telefono: str = Field(min_length=7, max_length=15)
    categorias: str | None = Field(default=None, max_length=255)
    imagen: str | None = Field(default=None, max_length=255)
    horario_atencion: time | None = Field(default=None)
    activo: bool

    class Config:
        json_schema = {
            "example": {
                "id_negocio": 1,
                "nombre": "La Taquería",
                "categoria": "Comida rápida",
                "rating": 4.5,
                "rango_precios": "50-100",
                "ubicacion": "Av. Universidad #123",
                "nombre_responsable": "Carlos López",
                "telefono": "5559876543",
                "categorias": "Mexicana, Tacos, Salsas",
                "imagen": "tacos.png",
                "horario_atencion": "10:00:00",
                "activo": True
            }
        }
