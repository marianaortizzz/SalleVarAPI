from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from schemas.producto_menu import ProductoMenu
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
@producto_router.get("/obtenerMenu", tags=["Productos"], response_model=List[ProductoMenu])
def get_productos(id_restaurante: int, db: Session = Depends(get_db)):
    productos = ProductoService(db).get_menu(id_restaurante)
    return productos


# Crear un nuevo producto
@producto_router.post("/agregarProductoAMenu", tags=["Productos"], response_model=ProductoMenu, status_code=201)
def create_producto(producto: ProductoMenu, db: Session = Depends(get_db)):
    producto_modificado = ProductoService(db).create_producto(producto)
    return producto_modificado

# Actualizar un producto existente
@producto_router.put("/editarProducto/{id_producto}", tags=["Productos"], response_model=ProductoMenu)
def update_producto(id_producto: int, producto: ProductoMenu, db: Session = Depends(get_db)):
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