from sqlalchemy import func
from SalleVarAPI.models import Estadistica as EstadisticaModel
from SalleVarAPI.schemas import Estadistica
from SalleVarAPI.models.detalle_pedido import DetallePedido as DetallePedidoModel
from SalleVarAPI.models.pedido import Pedido as PedidoModel
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
    
    def create_estadistica(self, id_restaurante: int):
        """
        Crear una estadística
        """
        estadistica = Estadistica()
        monto_total = self.db.query(DetallePedidoModel).join(PedidoModel).filter(
            PedidoModel.id_restaurante == id_restaurante,
        ).with_entities(func.sum(DetallePedidoModel.monto)).scalar() or 0
        estadistica.monto_total = float(monto_total)
        rating_promedio = self.db.query(DetallePedidoModel).join(PedidoModel).filter(
            PedidoModel.id_restaurante == id_restaurante,
        ).with_entities(func.avg(DetallePedidoModel.rating)).scalar() or 0
        estadistica.rating_promedio = float(rating_promedio)
        id_producto_mas_vendido = self.db.query(DetallePedidoModel.id_producto).join(PedidoModel).filter(
            PedidoModel.id_restaurante == id_restaurante,
        ).with_entities(func.count(DetallePedidoModel.id_producto)).order_by(func.count(DetallePedidoModel.id_producto).desc()).first()
        estadistica.id_producto_mas_vendido = id_producto_mas_vendido[0] if id_producto_mas_vendido else None
        numero_ventas = self.db.query(DetallePedidoModel).join(PedidoModel).filter(
            PedidoModel.id_restaurante == id_restaurante,
        ).with_entities(func.count(DetallePedidoModel.id_detalle_pedido)).scalar() or 0
        estadistica.numero_ventas = numero_ventas
        estadistica.id_restaurante = id_restaurante

        # Crear una nueva instancia del modelo Estadistica
        new_estadistica = EstadisticaModel(**estadistica.dict())

        # Agregar y guardar en la base de datos
        self.db.add(new_estadistica)
        self.db.commit()
        self.db.refresh(new_estadistica)

        return new_estadistica
    
    
    def delete_estadistica(self, id_estadistica: int):
        """
        Eliminar estadística
        """
        result = self.db.query(EstadisticaModel).filter(EstadisticaModel.id_estadistica == id_estadistica).delete()
        self.db.commit()
        return result