from pydantic import BaseModel

class RepartidorResponse(BaseModel):
    id_usuario: int
    nombre_completo: str
    telefono: str
    foto: str | None
    numero_pedidos: int
    rating_repartidor: float

    class Config:
        # orm_mode para que pydantic pueda trabajar con ORMs como SQLAlchemy
        # que es orm_mode?
        # es una configuracion que permite a pydantic trabajar con objetos ORM (Object Relational Mapper) y establecer que los modelos de pydantic pueden mapearse directamente a las tablas de la base de datos.
        orm_mode = True
        schema_extra = {
            "example": {
                "id_usuario": 1,
                "nombre_completo": "Juan Pérez",
                "telefono": "5551234567",
                "foto": "perfil1.jpg",
                "numero_pedidos": 50,
                "rating_repartidor": 4.5
            }
        }