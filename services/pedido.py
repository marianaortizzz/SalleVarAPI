from models.pedido import Pedido as PedidoModel
from schemas.pedido import Pedido

class PedidoService:
    def __init__(self, db) -> None:
        self.db = db
    
    def get_all(self):
        return self.db.query(PedidoModel).all()
    
    def get_by_id(self, campo: int):
        return self.db.query(PedidoModel).filter(PedidoModel.campo == campo).first()
    
    def create_pedido(self, pedido: Pedido):
        pedido_data = pedido.model_dump()

        new_pedido = PedidoModel(**pedido_data)
        self.db.add(new_pedido)
        self.db.commit()
        self.db.refresh(new_pedido)
        return new_pedido
    
    def update_pedido(self, campo: int, data: Pedido):
        pedido = self.db.query(PedidoModel).filter(PedidoModel.campo == campo).first()

        if not pedido:
            return None

        pedido.fecha_pedido = data.fecha_pedido
        pedido.status = data.status
        pedido.id_cliente = data.id_cliente
        pedido.id_negocio = data.id_negocio
        pedido.monto_total = data.monto_total
        pedido.status_pago = data.status_pago
        pedido.rating_pedido = data.rating_pedido

        self.db.commit()
        self.db.refresh(pedido)
        return pedido
    
    def delete_pedido(self, campo: int):
        result = self.db.query(PedidoModel).filter(PedidoModel.campo == campo).delete()
        self.db.commit()
        return result
