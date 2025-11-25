from pydantic import BaseModel

class FilterRequestModel(BaseModel):
    categoria: bool
    texto: bool
    valor: str

    class Config:
        from_attributes = True
        json_schema = {
            "example": {
                "categoria": True,
                "texto": False,
                "valor": "Comida"
            }
        }