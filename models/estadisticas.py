from sqlalchemy import Column, Integer, Date, Numeric, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Estadistica(Base):
    __tablename__ = 'estadisticas'

    id_estadistica = Column(Integer, primary_key=True, autoincrement=True)
    fecha_inicio = Column(Date, nullable=True)
    monto_total = Column(Numeric(10, 2), nullable=True)
    rating_promedio = Column(Numeric(2, 1), nullable=True)
    producto_mas_vendido = Column(String(255), nullable=True)
    numero_ventas = Column(Integer, nullable=True)
    
    id_restaurante = Column(Integer, ForeignKey('Negocio.id_negocio'), nullable=False)
    restaurante = relationship('Negocio', back_populates='estadisticas', foreign_keys=[id_restaurante])
