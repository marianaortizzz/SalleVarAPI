from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from config.database import Base
from sqlalchemy import (
    Column, Integer, ForeignKey, String, func
)
from models.opcion import OpcionModificador


class ModificadorProducto(Base):
    __tablename__ = "modificador_producto"

    id_modificador = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_modificador = Column(String(255), nullable=False)
    num_max_selec = Column(Integer, nullable=False, default=1)
    opciones = relationship(
        "OpcionModificador", 
        back_populates="modificador", 
        cascade="all, delete-orphan"
    )
    id_producto = Column(Integer, ForeignKey("producto.id_producto", ondelete="CASCADE"), nullable=False)


