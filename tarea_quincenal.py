from config.database import SessionLocal
from services.estadisticas import EstadisticaService

def main():
    db = SessionLocal()
    try:
        service = EstadisticaService(db)
        service.ejecutar_tarea_quincenal()
    finally:
        db.close()

if __name__ == "__main__":
    main()