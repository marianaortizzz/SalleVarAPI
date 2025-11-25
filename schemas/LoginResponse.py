from pydantic import BaseModel

class LoginResponse(BaseModel):
    status_code: int
    id_usuario: int | None = None
    mensaje: str

    class Config:
        schema_extra = {
            "example": {
                "status_code": 200,
                "id_usuario": 123,
                "mensaje": "Inicio de sesión exitoso"
            }
        }