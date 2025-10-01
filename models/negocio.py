from config.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, Enum, Time
class Negocio(Base):
    __tablename__ = "negocio"

    id_negocio = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(255))
    categoria = Column(Enum(''))  # ⚠️ Definir valores reales del enum
    rating = Column(DECIMAL)
    rango_precios = Column(Enum('0-50', '50-100', '100-150', '150-200', '+200'))
    ubicacion = Column(String(255))
    nombre_responsable = Column(String(255))
    telefono = Column(String(15))
    categorias = Column(String(255))
    imagen = Column(String(255))
    horario_atencion = Column(Time)
    activo = Column(Boolean)