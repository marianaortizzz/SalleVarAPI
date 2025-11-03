from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from config.database import SessionLocal
from schemas.pedido import Pedido
from services.pedido import PedidoService

pedido_router = APIRouter()

# Dependencia para manejar la sesión de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Obtener todos los pedidos
@pedido_router.get("/pedidos", tags=["Pedidos"], response_model=List[Pedido])
def get_pedidos(db: Session = Depends(get_db)):
    pedidos = PedidoService(db).get_all()
    return pedidos

# Obtener pedido por ID
@pedido_router.get("/pedidos/{pedido_id}", tags=["Pedidos"], response_model=Pedido)
def get_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = PedidoService(db).get_by_id(pedido_id)
    if pedido:
        return pedido
    raise HTTPException(status_code=404, detail="Pedido no encontrado")

# Crear nuevo pedido
@pedido_router.post("/pedidos", tags=["Pedidos"], response_model=Pedido, status_code=201)
def create_pedido(pedido: Pedido, db: Session = Depends(get_db)):
    nuevo_pedido = PedidoService(db).create_pedido(pedido)
    return nuevo_pedido

# Actualizar pedido existente
@pedido_router.put("/pedidos/{pedido_id}", tags=["Pedidos"], response_model=Pedido)
def update_pedido(pedido_id: int, pedido: Pedido, db: Session = Depends(get_db)):
    actualizado = PedidoService(db).update_pedido(pedido_id, pedido)
    if actualizado:
        return actualizado
    raise HTTPException(status_code=404, detail="Pedido no encontrado")

# Eliminar pedido por ID
@pedido_router.delete("/pedidos/{pedido_id}", tags=["Pedidos"])
def delete_pedido(pedido_id: int, db: Session = Depends(get_db)):
    success = PedidoService(db).delete_pedido(pedido_id)
    if success:
        return {"message": "Pedido eliminado"}
    raise HTTPException(status_code=404, detail="Pedido no encontrado")
