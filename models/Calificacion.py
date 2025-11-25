from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class Calificacion(Base):
    __tablename__ = "calificaciones"

    id_calificacion = Column(Integer, primary_key=True, index=True)
    id_origen = Column(Integer, ForeignKey("cliente.id_cliente"), nullable=False)
    id_destino = Column(Integer, nullable=False)   # cliente o negocio
    tipo_destino = Column(Integer, nullable=False) # 1 = usuario, 2 = repartidor, 3 = negocio
    rating = Column(Integer, nullable=False)
