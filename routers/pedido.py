from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from config.database import SessionLocal
from schemas.pedido import Pedido, PedidoCreate
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
@pedido_router.get("/obtenerPedidos", tags=["Pedidos"], response_model=List[Pedido])
def get_pedidos(id: int, tipo_cuenta: str, status: str,db: Session = Depends(get_db)):
    pedidos = PedidoService(db).get_all(id, tipo_cuenta, status)
    return pedidos

# Obtener pedido por ID
@pedido_router.get("/mostrarInfoPedido/{pedido_id}", tags=["Pedidos"], response_model=Pedido)
def get_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = PedidoService(db).get_by_id(pedido_id)
    if pedido:
        return pedido
    raise HTTPException(status_code=404, detail="Pedido no encontrado")


# Crear nuevo pedido
@pedido_router.post("/hacerPedido", tags=["Pedidos"], response_model=Pedido, status_code=201)
def create_pedido(pedido: PedidoCreate, db: Session = Depends(get_db)):
    nuevo_pedido = PedidoService(db).create_pedido(pedido)
    return nuevo_pedido

# Actualizar pedido existente
@pedido_router.put("/modificarStatusPedido/{pedido_id}", tags=["Pedidos"], response_model=Pedido)
def update_pedido(pedido_id: int, nuevo_status: str, tipo_cuenta: str, db: Session = Depends(get_db)):
    actualizado = PedidoService(db).update_pedido_status(pedido_id, nuevo_status, tipo_cuenta)
    return actualizado

@pedido_router.post("/verificarCodigoRestaurante/{pedido_id}", tags=["Pedidos"], response_model=bool)
def get_pedido(pedido_id: int, codigo1: str, codigo2: str, db: Session = Depends(get_db)):
    pedido = PedidoService(db).verificar_codigo_rest(pedido_id, codigo1, codigo2)
    if pedido:
        return pedido
    raise HTTPException(status_code=404, detail="Pedido no encontrado")

@pedido_router.post("/verificarCodigoRepartidor/{pedido_id}", tags=["Pedidos"], response_model=bool)
def get_pedido(pedido_id: int, codigo1: int, codigo2: int, db: Session = Depends(get_db)):
    pedido = PedidoService(db).verificar_codigo_rep(pedido_id, codigo1, codigo2)
    if pedido:
        return pedido
    raise HTTPException(status_code=404, detail="Pedido no encontrado")

# Eliminar pedido por ID
@pedido_router.delete("/pedidos/{pedido_id}", tags=["Pedidos"])
def delete_pedido(pedido_id: int, db: Session = Depends(get_db)):
    success = PedidoService(db).delete_pedido(pedido_id)
    if success:
        return {"message": "Pedido eliminado"}
    raise HTTPException(status_code=404, detail="Pedido no encontrado")
