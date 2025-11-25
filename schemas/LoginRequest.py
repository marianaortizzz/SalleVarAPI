from pydantic import BaseModel

class LoginRequest(BaseModel):
    usuario: str
    contrasena: str

    class Config:
        schema_extra = {
            "example": {
                "usuario": "usuario_ejemplo",
                "contrasena": "contrasena_ejemplo"
            }
        }