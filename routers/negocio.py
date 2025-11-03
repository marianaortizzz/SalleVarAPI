from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from config.database import SessionLocal
from schemas.negocio import Negocio
from services.negocio import NegocioService

negocio_router = APIRouter()

#Dependencia para manejar la sesión de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Obtener todos los negocios
@negocio_router.get("/negocios", tags=["Negocios"], response_model=List[Negocio])
def get_negocios(db: Session = Depends(get_db)):
    negocios = NegocioService(db).get_all()
    return negocios

#Obtener negocio por ID
@negocio_router.get("/negocios/{negocio_id}", tags=["Negocios"], response_model=Negocio)
def get_negocio(negocio_id: int, db: Session = Depends(get_db)):
    negocio = NegocioService(db).get_by_id(negocio_id)
    if negocio:
        return negocio
    raise HTTPException(status_code=404, detail="Negocio no encontrado")

#Crear nuevo negocio
@negocio_router.post("/negocios", tags=["Negocios"], response_model=Negocio, status_code=201)
def create_negocio(negocio: Negocio, db: Session = Depends(get_db)):
    nuevo_negocio = NegocioService(db).create_negocio(negocio)
    return nuevo_negocio

#Actualizar negocio existente
@negocio_router.put("/negocios/{negocio_id}", tags=["Negocios"], response_model=Negocio)
def update_negocio(negocio_id: int, negocio: Negocio, db: Session = Depends(get_db)):
    actualizado = NegocioService(db).update_negocio(negocio_id, negocio)
    if actualizado:
        return actualizado
    raise HTTPException(status_code=404, detail="Negocio no encontrado")

#Eliminar negocio por ID
@negocio_router.delete("/negocios/{negocio_id}", tags=["Negocios"])
def delete_negocio(negocio_id: int, db: Session = Depends(get_db)):
    success = NegocioService(db).delete_negocio(negocio_id)
    if success:
        return {"message": "Negocio eliminado"}
    raise HTTPException(status_code=404, detail="Negocio no encontrado")
