from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Producto(Base):
    __tablename__ = 'producto'

    id_producto = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=True)
    precio = Column(Numeric(10, 2), nullable=True)
    descripcion = Column(String(255), nullable=True)
    imagen = Column(String(255), nullable=True)
    categoria = Column(String(50), nullable=True)
    disponible = Column(Boolean, nullable=False, default=True)

    id_negocio = Column(Integer, ForeignKey('Negocio.id_negocio'), nullable=True)
    negocio = relationship('Negocio', back_populates='productos')