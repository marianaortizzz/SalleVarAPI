from pydantic import BaseModel


#Josa esto solo es un schema prueba, modificalo
class Repartidor(BaseModel):
    id_repartidor: str
    nombre: str
    telefono: str
    vehiculo: str

    class Config:
        json_schema = {
            "example": {
                "id_repartidor": "rep123",
                "nombre": "Juan Perez",
                "telefono": "555-1234",
                "vehiculo": "Moto"
            }
        }