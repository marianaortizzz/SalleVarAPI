from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from schemas.producto_menu import ProductoMenu
from config.database import SessionLocal
from schemas.producto import Producto, ProductoCreate, ProductoUpdate
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
@producto_router.get("/obtenerMenu", tags=["Productos"], response_model=List[Producto])
def get_productos(id_restaurante: int, db: Session = Depends(get_db)):
    productos = ProductoService(db).get_menu(id_restaurante)
    return productos
    
    
# Crear un nuevo producto
@producto_router.post("/agregarProductoAMenu", tags=["Productos"], response_model=Producto, status_code=201)
def create_producto(producto: ProductoCreate, id_negocio: int, db: Session = Depends(get_db)):
    producto_modificado = ProductoService(db).create_producto_completo(product_data= producto, id_negocio=id_negocio)
    return producto_modificado

# Actualizar un producto existente
@producto_router.put("/editarProducto/{id_producto}", tags=["Productos"], response_model=Producto)
def update_producto(id_producto: int, producto: ProductoUpdate, db: Session = Depends(get_db)):
    producto = ProductoService(db).update_producto_completo(id_producto, producto)
    if producto is not None:
        return producto
    raise HTTPException(status_code=404, detail="Producto no encontrado")

# Eliminar un producto por ID
@producto_router.delete("/productos/{id_producto}", tags=["Productos"])
def delete_producto(id_producto: int, db: Session = Depends(get_db)):
    success = ProductoService(db).delete_producto(id_producto)
    if success:
        return {"message": "Producto eliminado"}
    raise HTTPException(status_code=404, detail="Producto no encontrado")