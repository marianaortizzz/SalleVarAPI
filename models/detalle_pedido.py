from config.database import Base
from sqlalchemy import Column, Integer, DECIMAL, ForeignKey, String
from sqlalchemy.orm import relationship

class DetallePedido(Base):
    __tablename__ = "detalle_pedido"

    id_detalle_pedido = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_pedido = Column(Integer, ForeignKey('pedido.id_pedido'))
    pedido = relationship("Pedido", back_populates="detalles")
    id_producto = Column(Integer, ForeignKey('producto.id_producto'))
    producto = relationship("Producto", back_populates="detalles")
    cantidad = Column(Integer)
    precio_unitario = Column(DECIMAL(10, 2))
    rating = Column(DECIMAL(2, 1), nullable=True)
    opciones = Column(String(255), nullable=True)
    comentarios = Column(String(255), nullable=True)
    total_producto = Column(DECIMAL(10, 2),  nullable=True)
    # Relationship to the Pedido object
    

    # Relationship to the Producto object
    
