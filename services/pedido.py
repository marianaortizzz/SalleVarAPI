from datetime import datetime
from decimal import Decimal
from typing import List
from models.detalle_pedido import DetallePedido
from models.pedido import Pedido as PedidoModel
from schemas.pedido import Pedido as PedidoSchema
from schemas.pedido import PedidoCreate
from schemas.detalle_pedido import DetallePedidoCreate
from models.detalle_pedido import DetallePedido as DetallePedidoModel
from sqlalchemy.orm import joinedload as joinLoaded
from schemas.producto_pedido import ProductoPedido as ProductoSchema
from models.producto import Producto as ProductoModel
class PedidoService:
    def __init__(self, db) -> None:
        self.db = db
    def get_all(self, id: int, tipo_cuenta: str, status: str) -> List[PedidoSchema]:
        """
        Obtiene todos los pedidos asociados a un ID específico según el tipo de cuenta y el estado general.
        """
        if tipo_cuenta == "cliente":
            if(status=="activos"):
                pedidos = self.db.query(PedidoModel).filter(
                    PedidoModel.id_cliente == id, 
                    PedidoModel.status_general.in_(["Pendiente", "En_proceso"])
                ).options(joinLoaded(PedidoModel.detalles)).all()
            else:
                pedidos = self.db.query(PedidoModel).filter(
                    PedidoModel.id_cliente == id, 
                    PedidoModel.status_general.in_(["Completado", "Cancelado"])
                ).options(joinLoaded(PedidoModel.detalles)).all()
            for pedido in pedidos:
                for detalle in pedido.detalles:
                    producto = self.db.query(ProductoModel).filter(ProductoModel.id_producto == detalle.id_producto).first()
                    detalle.nombre = producto.nombre
                    detalle.descripcion = producto.descripcion
            return pedidos
        elif tipo_cuenta == "negocio":
            pedidos = self.db.query(PedidoModel).filter(
                PedidoModel.id_negocio == id, 
                PedidoModel.status_rest == status
            ).options(joinLoaded(PedidoModel.detalles)).all()
            for pedido in pedidos:
                for detalle in pedido.detalles:
                    producto = self.db.query(ProductoModel).filter(ProductoModel.id_producto == detalle.id_producto).first()
                    detalle.nombre = producto.nombre
                    detalle.descripcion = producto.descripcion
            return pedidos
        elif tipo_cuenta == "repartidor":
            pedidos = self.db.query(PedidoModel).filter(
                PedidoModel.id_repartidor == id, 
                PedidoModel.status_rep == status
            ).options(joinLoaded(PedidoModel.detalles)).all()
            for pedido in pedidos:
                for detalle in pedido.detalles:
                    producto = self.db.query(ProductoModel).filter(ProductoModel.id_producto == detalle.id_producto).first()
                    detalle.nombre = producto.nombre
                    detalle.descripcion = producto.descripcion
            return pedidos
        else:
            return []
    
    def get_by_id(self, pedido_id: int) -> PedidoSchema:
        """
        Obtiene un pedido por su ID.
        """
        pedido= self.db.query(PedidoModel).filter(PedidoModel.id_pedido == pedido_id).options(joinLoaded(PedidoModel.detalles)).first()
        for detalle in pedido.detalles:
            producto = self.db.query(ProductoModel).filter(ProductoModel.id_producto == detalle.id_producto).first()
            detalle.nombre = producto.nombre
            detalle.descripcion = producto.descripcion
        return pedido
    
    def create_pedido(self, pedido_data: PedidoCreate) -> PedidoSchema:
        """
        Crea un nuevo pedido, incluyendo los registros en DetallePedido.
        """
        detalles_data: List[DetallePedidoCreate] = pedido_data.detalles
        pedido_fields = pedido_data.model_dump(exclude={"detalles"})
        db_pedido = PedidoModel(**pedido_fields) 
        for detalle_in in detalles_data:
            db_detalle = DetallePedidoModel(**detalle_in.model_dump())
            db_pedido.detalles.append(db_detalle)

        self.db.add(db_pedido)
        self.db.commit() 
        self.db.refresh(db_pedido) 
        for detalle in db_pedido.detalles:
            producto = self.db.query(ProductoModel).filter(ProductoModel.id_producto == detalle.id_producto).first()
            detalle.nombre = producto.nombre
            detalle.descripcion = producto.descripcion

        return db_pedido
    
    def update_pedido_status(self, pedido_id: int, nuevo_status: str, tipo_cuenta: str) -> PedidoSchema:
        """
        Actualiza el estado general de un pedido por su ID.
        """
        if tipo_cuenta == "negocio":
            pedido = self.db.query(PedidoModel).filter(PedidoModel.id_pedido == pedido_id).first()
            if not pedido:
                return None
            pedido.status_rest = nuevo_status
            self.db.commit()
            self.db.refresh(pedido)
            for detalle in pedido.detalles:
                producto = self.db.query(ProductoModel).filter(ProductoModel.id_producto == detalle.id_producto).first()
                detalle.nombre = producto.nombre
                detalle.descripcion = producto.descripcion
            return pedido
        elif tipo_cuenta == "repartidor":
            pedido = self.db.query(PedidoModel).filter(PedidoModel.id_pedido == pedido_id).first()
            if not pedido:
                return None
            pedido.status_rep = nuevo_status
            self.db.commit()
            self.db.refresh(pedido)
            for detalle in pedido.detalles:
                producto = self.db.query(ProductoModel).filter(ProductoModel.id_producto == detalle.id_producto).first()
                detalle.nombre = producto.nombre
                detalle.descripcion = producto.descripcion
            return pedido
        elif tipo_cuenta == "cliente":
            pedido = self.db.query(PedidoModel).filter(PedidoModel.id_pedido == pedido_id).first()
            if not pedido:
                return None
            pedido.status_general = nuevo_status
            self.db.commit()
            self.db.refresh(pedido)
            for detalle in pedido.detalles:
                producto = self.db.query(ProductoModel).filter(ProductoModel.id_producto == detalle.id_producto).first()
                detalle.nombre = producto.nombre
                detalle.descripcion = producto.descripcion
            return pedido
        else:
            return None
        
    
    def verificar_codigo_rest(self, pedido_id: int, codigo_rest: str, codigo_rep: str) -> bool:
        """
        Verifica el código del restaurante y el del repartidor para un pedido específico.
        Los códigos se esperan como strings (str).
        """
        pedido = self.db.query(PedidoModel).filter(PedidoModel.id_pedido == pedido_id).first()

        if not pedido:
            return False
        
        # Comparación de códigos como strings
        if str(pedido.codigo_rest) == codigo_rest and str(pedido.codigo_rep) == codigo_rep:
            return True
        else:
            return False
        
    def verificar_codigo_rep(self, pedido_id: int, codigo_rep: str, codigo_rest: str) -> bool:
        """
        Verifica el código del repartidor y el del restaurante para un pedido específico.
        Los códigos se esperan como strings (str).
        """
        pedido = self.db.query(PedidoModel).filter(PedidoModel.id_pedido == pedido_id).first()

        if not pedido:
            return False
        
        # Comparación de códigos como strings
        if str(pedido.codigo_rep) == codigo_rep and str(pedido.codigo_rest) == codigo_rest:
            return True
        else:
            return False
    
    def delete_pedido(self, pedido_id: int) -> int:
        """
        Elimina un pedido por su ID. La cascada eliminará los detalles asociados.
        Retorna el número de filas eliminadas (0 o 1).
        """
        result = self.db.query(PedidoModel).filter(PedidoModel.id_pedido == pedido_id).delete(synchronize_session=False)
        self.db.commit()
        return result
    
    def get_producto_by_id(self, producto_id: int) -> ProductoModel:
        
        return self.db.query(ProductoModel).filter(ProductoModel.id_producto == producto_id).first()
