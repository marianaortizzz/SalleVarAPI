from config.database import Base
from sqlalchemy import Column, Integer, DECIMAL, ForeignKey

class DetallePedido(Base):
    __tablename__ = "detalle_pedido"

    id_detalle_pedido = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_pedido = Column(Integer, ForeignKey('pedido.id_pedido'))
    id_producto = Column(Integer, ForeignKey('producto.id_producto'))
    cantidad = Column(Integer)
    precio_unitario = Column(DECIMAL(10, 2))
