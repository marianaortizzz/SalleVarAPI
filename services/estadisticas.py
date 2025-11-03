from SalleVarAPI.models import Estadistica as EstadisticaModel
from SalleVarAPI.schemas import Estadistica
class EstadisticaService:
    def __init__(self, db) -> None:
        self.db = db
    def get_all(self):
        """
        Obtener todas las estadísticas
        """
        return self.db.query(EstadisticaModel).all()
    
    def get_by_id(self, id_estadistica: int):
        """
        Obtener estadística por id
        """
        return self.db.query(EstadisticaModel).filter(EstadisticaModel.id_estadistica == id_estadistica).first()
    
    def create_estadistica(self, estadistica: Estadistica):
        """
        Crear una estadística
        """
        estadistica_data = estadistica.model_dump()

        new_estadistica = EstadisticaModel(**estadistica_data)
        self.db.add(new_estadistica)
        self.db.commit()
        self.db.refresh(new_estadistica)
        return new_estadistica
    
    def update_estadistica(self, id_estadistica: int, data: Estadistica):
        """
        Actualizar estadística
        """
        estadistica = self.db.query(EstadisticaModel).filter(EstadisticaModel.id_estadistica == id_estadistica).first()

        if not estadistica:
            return None
        
        estadistica.fecha_inicio = data.fecha_inicio
        estadistica.monto_total = data.monto_total
        estadistica.rating_promedio = data.rating_promedio
        estadistica.producto_mas_vendido = data.producto_mas_vendido
        estadistica.numero_ventas = data.numero_ventas

        self.db.commit()
        self.db.refresh(estadistica)
        return estadistica
    
    def delete_estadistica(self, id_estadistica: int):
        """
        Eliminar estadística
        """
        result = self.db.query(EstadisticaModel).filter(EstadisticaModel.id_estadistica == id_estadistica).delete()
        self.db.commit()
        return result