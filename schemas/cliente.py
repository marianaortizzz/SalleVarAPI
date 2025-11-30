from pydantic import BaseModel, Field, field_validator, ConfigDict
import ast
from typing import Any, Optional

class Cliente(BaseModel):
    id_cliente: int | None = Field(default=None)
    nombre_completo: str = Field(min_length=1, max_length=255)
    matricula: int = Field(ge=1, le=999999)
    carrera: str = Field(min_length=1, max_length=255)
    repartidor: bool
    negocios_favoritos: list[str] = Field(default=[])
    contrasena: Optional[str] = Field(default=None, max_length=64)
    foto: str | None = Field(default=None, max_length=255)
    telefono: str = Field(min_length=7, max_length=15)
    edificio : str | None = Field(default=None) 
    salon : int | None = Field(default=None)
    calificacion_cliente: int | None = Field(default=None)
    calificacion_repartidor: int | None = Field(default=None)

    @field_validator('negocios_favoritos', mode='before')
    @classmethod
    def parsear_lista(cls, v: Any) -> list[str]:
        # Si el valor es un string (viene de la BD así), lo convertimos
        if isinstance(v, str):
            try:
                # ast.literal_eval es capaz de entender "['A', 'B']"
                return ast.literal_eval(v)
            except (ValueError, SyntaxError):
                # Si falla la conversión, devolvemos lista vacía para no romper la API
                return []
        # Si ya es una lista o es None, lo dejamos pasar
        return v if v is not None else []

    class Config:
        from_attributes = True
        json_schema = {
            "example": {
                "id_cliente": 1,
                "nombre_completo": "Juan Pérez",
                "matricula": 1234,
                "carrera": "Ingeniería en Sistemas",
                "repartidor": False,
                "negocios_favoritos": [],
                "contrasena": "12345678",
                "foto": "perfil1.jpg",
                "telefono": "5551234567", 
                "edificio": "A",
                "salon": 101,
                "calificacion_cliente": 5,
                "calificacion_repartidor": None
            }
        }
