from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from config.database import SessionLocal
from schemas.detalle_pedido import DetallePedido
from services.detalle_pedido import DetallePedidoService

detalle_pedido_router = APIRouter()

# Dependencia para manejar la sesión de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Obtener todos los detalles pedido
@detalle_pedido_router.get("/detalles-pedidos", tags=["Detalles Pedidos"], response_model=List[DetallePedido])
def get_detalles_pedidos(db: Session = Depends(get_db)):
    detalles = DetallePedidoService(db).get_all()
    return detalles

# Obtener detalles de un pedido específico
@detalle_pedido_router.get("/pedidos/{pedido_id}/detalles", tags=["Detalles Pedidos"], response_model=List[DetallePedido])
def get_detalles_by_pedido(pedido_id: int, db: Session = Depends(get_db)):
    detalles = DetallePedidoService(db).get_by_pedido(pedido_id)
    return detalles

# Obtener detalle pedido por ID
@detalle_pedido_router.get("/detalles-pedidos/{detalle_id}", tags=["Detalles Pedidos"], response_model=DetallePedido)
def get_detalle_pedido(detalle_id: int, db: Session = Depends(get_db)):
    detalle = DetallePedidoService(db).get_by_id(detalle_id)
    if detalle:
        return detalle
    raise HTTPException(status_code=404, detail="Detalle de pedido no encontrado")

# Crear detalle pedido
@detalle_pedido_router.post("/detalles-pedidos", tags=["Detalles Pedidos"], response_model=DetallePedido, status_code=201)
def create_detalle_pedido(detalle_pedido: DetallePedido, db: Session = Depends(get_db)):
    nuevo_detalle = DetallePedidoService(db).create_detalle_pedido(detalle_pedido)
    return nuevo_detalle

# Actualizar detalle pedido existente
@detalle_pedido_router.put("/detalles-pedidos/{detalle_id}", tags=["Detalles Pedidos"], response_model=DetallePedido)
def update_detalle_pedido(detalle_id: int, detalle_pedido: DetallePedido, db: Session = Depends(get_db)):
    actualizado = DetallePedidoService(db).update_detalle_pedido(detalle_id, detalle_pedido)
    if actualizado:
        return actualizado
    raise HTTPException(status_code=404, detail="Detalle de pedido no encontrado")

# Eliminar detalle pedido por ID
@detalle_pedido_router.delete("/detalles-pedidos/{detalle_id}", tags=["Detalles Pedidos"])
def delete_detalle_pedido(detalle_id: int, db: Session = Depends(get_db)):
    success = DetallePedidoService(db).delete_detalle_pedido(detalle_id)
    if success:
        return {"message": "Detalle de pedido eliminado"}
    raise HTTPException(status_code=404, detail="Detalle de pedido no encontrado")
