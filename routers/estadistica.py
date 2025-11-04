from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from config.database import SessionLocal
from schemas.estadisticas import Estadistica
from services.estadisticas import EstadisticaService

estadistica_router = APIRouter()

# Dependencia para obtener la sesión de la DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Obtener todas las estadísticas
@estadistica_router.get("/estadisticas", tags=["Estadísticas"], response_model=List[Estadistica])
def get_estadisticas(db: Session = Depends(get_db)):
    estadisticas = EstadisticaService(db).get_all()
    return estadisticas

# Obtener una estadística por ID
@estadistica_router.get("/estadisticas/{id_estadistica}", tags=["Estadísticas"], response_model=Estadistica)
def get_estadistica(id_estadistica: int, db: Session = Depends(get_db)):
    estadistica = EstadisticaService(db).get_by_id(id_estadistica)
    if estadistica:
        return estadistica
    raise HTTPException(status_code=404, detail="Estadística no encontrada")

# Crear una nueva estadística
@estadistica_router.post("/estadisticas", tags=["Estadísticas"], response_model=Estadistica, status_code=201)
def create_estadistica(estadistica: Estadistica, db: Session = Depends(get_db)):
    nueva_estadistica = EstadisticaService(db).create_estadistica(estadistica)
    return nueva_estadistica


# Eliminar una estadística por ID
@estadistica_router.delete("/estadisticas/{id_estadistica}", tags=["Estadísticas"])
def delete_estadistica(id_estadistica: int, db: Session = Depends(get_db)):
    success = EstadisticaService(db).delete_estadistica(id_estadistica)
    if success:
        return {"message": "Estadística eliminada"}
    raise HTTPException(status_code=404, detail="Estadística no encontrada")