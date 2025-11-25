from pydantic import BaseModel, Field

class CalificarModel(BaseModel):
    id_origen: int
    id_destino: int
    tipo_destino: int = Field(..., description="1=usuario, 2=repartidor, 3=negocio")
    rating: int = Field(ge=1, le=5)

    class Config:
        json_schema = {
            "example": {
                "id_origen": 1,
                "id_destino": 2,
                "tipo_destino": 2,
                "rating": 5
            }
        }