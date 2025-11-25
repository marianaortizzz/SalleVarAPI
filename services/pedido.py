from models.pedido import Pedido as PedidoModel
from schemas.pedido import Pedido

class PedidoService:
    def __init__(self, db) -> None:
        self.db = db
    
    def get_all(self, id: int, tipo_cuenta: str, status: str):
        if tipo_cuenta == "cliente":
            return self.db.query(PedidoModel).filter(PedidoModel.id_cliente == id, PedidoModel.status_general == status).all()
        elif tipo_cuenta == "negocio":
            return self.db.query(PedidoModel).filter(PedidoModel.id_negocio == id, PedidoModel.status_general == status).all()
        elif tipo_cuenta == "repartidor":
            return self.db.query(PedidoModel).filter(PedidoModel.id_repartidor == id, PedidoModel.status_general == status).all()
        else:
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
    
    def update_pedido(self, campo: int, nuevo_status: str):
        pedido = self.db.query(PedidoModel).filter(PedidoModel.campo == campo).first()

        if not pedido:
            return None
        
        pedido.status_general = nuevo_status

        self.db.commit()
        self.db.refresh(pedido)
        return pedido
    
    def verificar_codigo_rest(self, campo: int, codigo1: int, codigo2: int):
        pedido = self.db.query(PedidoModel).filter(PedidoModel.campo == campo).first()

        if not pedido:
            return None
        
        if pedido.codigo_rest == codigo1 and pedido.codigo_rep == codigo2:
            return pedido
        else:
            return None
        
    def verificar_codigo_rep(self, campo: int, codigo1: int, codigo2: int):
        pedido = self.db.query(PedidoModel).filter(PedidoModel.campo == campo).first()

        if not pedido:
            return None
        
        if pedido.codigo_rep == codigo1 and pedido.codigo_rest == codigo2:
            return pedido
        else:
            return None
    
    def delete_pedido(self, campo: int):
        result = self.db.query(PedidoModel).filter(PedidoModel.campo == campo).delete()
        self.db.commit()
        return result
