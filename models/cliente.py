from config.database import Base
from sqlalchemy import Column, Integer, String, Boolean, SmallInteger, JSON

class Cliente(Base):
    __tablename__ = "cliente"

    id_cliente = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_completo = Column(String(255))
    matricula = Column(SmallInteger)
    carrera = Column(String(255))
    repartidor = Column(Boolean)
    negocios_favoritos = Column(JSON)
    contrasena = Column(String(64))
    foto = Column(String(255))
    telefono = Column(String(15))
    edificio = Column(String(1))
    salon = Column(SmallInteger)
    calificacion_cliente = Column(SmallInteger)
    calificacion_repartidor = Column(SmallInteger)