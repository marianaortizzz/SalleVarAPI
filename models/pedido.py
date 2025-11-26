from config.database import Base
from sqlalchemy import Column, Integer, String, Date, DECIMAL, Enum, ForeignKey, Boolean
from sqlalchemy.orm import relationship

class Pedido(Base):
    __tablename__ = "pedido"

    id_pedido = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fecha_pedido = Column(Date)
    status_general = Column(Enum('Pendiente', 'En_proceso', 'Completado', 'Cancelado'))
    status_rest = Column(Enum('Pendiente', 'Preparando', 'Listo'))
    status_rep = Column(Enum('Asignado', 'En_camino', 'Entregado'))
    id_cliente = Column(Integer, ForeignKey('cliente.id_cliente'))
    id_negocio = Column(Integer, ForeignKey('negocio.id_negocio'))
    id_repartidor = Column(Integer, ForeignKey('repartidor.id_repartidor'), nullable=True)
    subtotal = Column(DECIMAL(10, 2))
    costo_envio = Column(DECIMAL(10, 2))
    costo_servicio = Column(DECIMAL(10, 2))
    monto_total = Column(DECIMAL(10, 2))
    status_pago = Column(Enum('Pendiente', 'Pagado', 'Rechazado'))
    rating_pedido = Column(DECIMAL(2, 1), nullable=True)
    rating_rep = Column(DECIMAL(2, 1), nullable=True)
    codigo_rest = Column(String(50))
    codigo_rep = Column(String(50))
    para_llevar = Column(Boolean, default=False)
    comentarios = Column(String(255), nullable=True)
    delivery = Column(Boolean, default=True)

    detalles = relationship(
        "DetallePedido",
        back_populates="pedido",
        cascade="all, delete-orphan"
    )

    productos = relationship(
        "Producto",
        secondary="detalle_pedido", 
        back_populates="pedidos"
    )
