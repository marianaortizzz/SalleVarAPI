from fastapi import APIRouter
from fastapi.responses import JSONResponse
from config.database import SessionLocal
from schemas.negocio import Negocio
from services.negocio import NegocioService

negocio_router = APIRouter()

@negocio_router.get("/negocios", tags=["Negocios"], response_model=Negocio)
def get_negocios():
    """
    Obtener todos los negocios.
    """
    db = SessionLocal()
    result = NegocioService(db).get_negocios()
    return JSONResponse(content={"negocios": result}, status_code=200)

@negocio_router.get("/negocios/{negocio_id}", tags=["Negocios"], response_model=Negocio)
def get_negocio(negocio_id: int):
    """
    Obtener un negocio por su ID.
    """
    db = SessionLocal()
    result = NegocioService(db).get_negocio(negocio_id)
    if result:
        return JSONResponse(content={"negocio": result}, status_code=200)
    return JSONResponse(content={"message": "Negocio no encontrado"}, status_code=404)

@negocio_router.post("/negocios", tags=["Negocios"], response_model=Negocio)
def create_negocio(negocio: Negocio):
    """
    Crear un nuevo negocio.
    """
    db = SessionLocal()
    result = NegocioService(db).create_negocio(negocio)
    return JSONResponse(content={"negocio": result}, status_code=201)

@negocio_router.put("/negocios/{negocio_id}", tags=["Negocios"], response_model=Negocio)
def update_negocio(negocio_id: int, negocio: Negocio):
    """
    Actualizar un negocio existente.
    """
    db = SessionLocal()
    result = NegocioService(db).update_negocio(negocio_id, negocio)
    if result:
        return JSONResponse(content={"negocio": result}, status_code=200)
    return JSONResponse(content={"message": "Negocio no encontrado"}, status_code=404)

@negocio_router.delete("/negocios/{negocio_id}", tags=["Negocios"])
def delete_negocio(negocio_id: int):
    """
    Eliminar un negocio por su ID.
    """
    db = SessionLocal()
    success = NegocioService(db).delete_negocio(negocio_id)
    if success:
        return JSONResponse(content={"message": "Negocio eliminado"}, status_code=200)
    return JSONResponse(content={"message": "Negocio no encontrado"}, status_code=404)