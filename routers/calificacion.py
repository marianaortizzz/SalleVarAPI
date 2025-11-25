from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import SessionLocal
from schemas.CalificarModel import CalificarModel
from services.CalificacionService import CalificacionService

router_calificaciones = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router_calificaciones.post("/calificar")
def calificar(data: CalificarModel, db: Session = Depends(get_db)):
    service = CalificacionService(db)
    result, error = service.calificar(data)

    if error:
        return {"status_code": 400, "detail": error}
    
    return {"status_code": 200, "message": "Calificación registrada"}
