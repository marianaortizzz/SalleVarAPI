from sqlalchemy.orm import relationship
from config.database import Base

# /c:/Users/maria/OneDrive/Administración de proyectos/SalleVar/SalleVarAPI/models/opcion.py
from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    Boolean,
    ForeignKey,
    DateTime,
    func,
)



class OpcionModificador(Base):
    __tablename__ = "opciones_modificador"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(String(1024), nullable=True)
    precio = Column(Numeric(10, 2), nullable=False, default=0)
    disponible = Column(Boolean, nullable=False, default=True)
    modificador_id = Column(
        Integer, ForeignKey("modificador_producto.id_modificador", ondelete="CASCADE"), nullable=False
    )
    modificador = relationship("ModificadorProducto", back_populates="opciones")
