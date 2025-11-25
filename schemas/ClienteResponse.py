from pydantic import BaseModel

# devolver la informacion del cliente sin la contrasena
class ClienteResponse(BaseModel):
    id_cliente: int
    nombre_completo: str
    matricula: int
    carrera: str
    repartidor: bool
    negocios_favoritos: list[int]
    foto: str | None
    telefono: str
    edificio: str
    salon: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id_cliente": 1,
                "nombre_completo": "Juan Pérez",
                "matricula": 1234,
                "carrera": "Ingeniería en Sistemas",
                "repartidor": False,
                "negocios_favoritos": [1, 2, 3],
                "foto": "perfil1.jpg",
                "telefono": "5551234567",
                "edificio": "A",
                "salon": 101
            }
        }