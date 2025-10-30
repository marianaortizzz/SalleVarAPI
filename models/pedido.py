from config.database import Base
from sqlalchemy import Column, Integer, String, Date, DECIMAL, Enum, ForeignKey

class Pedido(Base):
    __tablename__ = "pedido"

    campo = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fecha_pedido = Column(Date)
    status = Column(Enum('Pendiente', 'En_proceso', 'Completado', 'Cancelado'))
    id_cliente = Column(Integer, ForeignKey('cliente.id_cliente'))
    id_negocio = Column(Integer, ForeignKey('negocio.id_negocio'))
    monto_total = Column(DECIMAL(10, 2))
    status_pago = Column(Enum('Pendiente', 'Pagado', 'Rechazado'))
    rating_pedido = Column(DECIMAL(2, 1))
