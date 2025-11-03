from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from config.database import SessionLocal
from schemas.producto import Producto
from services.producto import ProductoService

producto_router = APIRouter()

# Dependencia para obtener la sesión de la DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Obtener todos los productos
@producto_router.get("/productos", tags=["Productos"], response_model=List[Producto])
def get_productos(db: Session = Depends(get_db)):
    productos = ProductoService(db).get_all()
    return productos

# Obtener un producto por ID
@producto_router.get("/productos/{id_producto}", tags=["Productos"], response_model=Producto)
def get_producto(id_producto: int, db: Session = Depends(get_db)):
    producto = ProductoService(db).get_by_id(id_producto)
    if producto:
        return producto
    raise HTTPException(status_code=404, detail="Producto no encontrado")

# Crear un nuevo producto
@producto_router.post("/productos", tags=["Productos"], response_model=Producto, status_code=201)
def create_producto(producto: Producto, db: Session = Depends(get_db)):
    nuevo_producto = ProductoService(db).create_producto(producto)
    return nuevo_producto

# Actualizar un producto existente
@producto_router.put("/productos/{id_producto}", tags=["Productos"], response_model=Producto)
def update_producto(id_producto: int, producto: Producto, db: Session = Depends(get_db)):
    actualizado = ProductoService(db).update_producto(id_producto, producto)
    if actualizado:
        return actualizado
    raise HTTPException(status_code=404, detail="Producto no encontrado")

# Eliminar un producto por ID
@producto_router.delete("/productos/{id_producto}", tags=["Productos"])
def delete_producto(id_producto: int, db: Session = Depends(get_db)):
    success = ProductoService(db).delete_producto(id_producto)
    if success:
        return {"message": "Producto eliminado"}
    raise HTTPException(status_code=404, detail="Producto no encontrado")