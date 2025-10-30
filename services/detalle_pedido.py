from models.detalle_pedido import DetallePedido as DetallePedidoModel
from schemas.detalle_pedido import DetallePedido

class DetallePedidoService:
    def __init__(self, db) -> None:
        self.db = db
    
    def get_all(self):
        return self.db.query(DetallePedidoModel).all()
    
    def get_by_id(self, id_detalle_pedido: int):
        return self.db.query(DetallePedidoModel).filter(DetallePedidoModel.id_detalle_pedido == id_detalle_pedido).first()
    
    def get_by_pedido(self, id_pedido: int):
        return self.db.query(DetallePedidoModel).filter(DetallePedidoModel.id_pedido == id_pedido).all()
    
    def create_detalle_pedido(self, detalle_pedido: DetallePedido):
        detalle_data = detalle_pedido.model_dump()
        new_detalle = DetallePedidoModel(**detalle_data)
        self.db.add(new_detalle)
        self.db.commit()
        self.db.refresh(new_detalle)
        return new_detalle
    
    def update_detalle_pedido(self, id_detalle_pedido: int, data: DetallePedido):
        detalle = self.db.query(DetallePedidoModel).filter(DetallePedidoModel.id_detalle_pedido == id_detalle_pedido).first()

        if not detalle:
            return None

        detalle.id_pedido = data.id_pedido
        detalle.id_producto = data.id_producto
        detalle.cantidad = data.cantidad
        detalle.precio_unitario = data.precio_unitario
        self.db.commit()
        self.db.refresh(detalle)
        return detalle

    def delete_detalle_pedido(self, id_detalle_pedido: int):
        result = self.db.query(DetallePedidoModel).filter(DetallePedidoModel.id_detalle_pedido == id_detalle_pedido).delete()
        self.db.commit()
        return result
