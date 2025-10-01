from pydantic import BaseModel, Field

class Cliente(BaseModel):
    nombre_completo: str = Field(min_length=1, max_length=255)
    matricula: int = Field(ge=1, le=9999)
    carrera: str = Field(min_length=1, max_length=255)
    repartidor: bool
    negocios_favoritos: str | None = Field(default=None, max_length=255)
    contrasena: str = Field(min_length=6, max_length=64)
    foto: str | None = Field(default=None, max_length=255)
    telefono: str = Field(min_length=7, max_length=15)

    class Config:
        json_schema = {
            "example": {
                "id_cliente": 1,
                "nombre_completo": "Juan Pérez",
                "matricula": 1234,
                "carrera": "Ingeniería en Sistemas",
                "repartidor": False,
                "negocios_favoritos": "Pizza Hut, Starbucks",
                "contrasena": "12345678",
                "foto": "perfil1.jpg",
                "telefono": "5551234567"
            }
        }
