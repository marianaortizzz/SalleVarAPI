from pydantic import BaseModel, Field

class Cliente(BaseModel):
    id_cliente: int | None = Field(default=None)
    nombre_completo: str = Field(min_length=1, max_length=255)
    matricula: int = Field(ge=1, le=999999)
    carrera: str = Field(min_length=1, max_length=255)
    repartidor: bool
    negocios_favoritos: list[str] = Field(default=[])
    contrasena: str = Field(min_length=6, max_length=64)
    foto: str | None = Field(default=None, max_length=255)
    telefono: str = Field(min_length=7, max_length=15)
    edificio : str = Field(min_length=1, max_length=1)
    salon : int = Field(ge=1, le=999)
    calificacion_cliente: int | None = Field(default=None)
    calificacion_repartidor: int | None = Field(default=None)

    class Config:
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
