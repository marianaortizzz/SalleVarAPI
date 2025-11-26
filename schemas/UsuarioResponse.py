from pydantic import BaseModel

class UsuarioResponse(BaseModel):
    id_usuario: int
    nombre_usuario: str
    nombre_completo: str
    matricula: int
    carrera: str
    negocio_favorito: list[str] | None
    foto: str | None
    telefono: str
    edificio: str
    salon: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id_usuario": 1,
                "nombre_usuario": "usuario_ejemplo",
                "nombre_completo": "Juan Pérez",
                "matricula": 1234,
                "carrera": "Ingeniería en Sistemas",
                "negocio_favorito": "Negocio Ejemplo",
                "foto": "perfil1.jpg",
                "telefono": "5551234567",
                "edificio": "A",
                "salon": 101
            }
        }