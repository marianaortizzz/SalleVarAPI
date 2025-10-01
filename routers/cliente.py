from fastapi import APIRouter
from fastapi.responses import JSONResponse
from config.database import SessionLocal
from schemas.cliente import Cliente
from services.cliente import ClienteService

cliente_router = APIRouter()

@cliente_router.get("/clientes", tags=["Clientes"], response_model=Cliente)
def get_clientes():
    """
    Obtener todos los clientes.
    """
    db = SessionLocal()
    result = ClienteService(db).get_clientes()
    return JSONResponse(content={"clientes": result}, status_code=200)

@cliente_router.get("/clientes/{cliente_id}", tags=["Clientes"], response_model=Cliente)
def get_cliente(cliente_id: int):
    """
    Obtener un cliente por su ID.
    """
    db = SessionLocal()
    result = ClienteService(db).get_cliente(cliente_id)
    if result:
        return JSONResponse(content={"cliente": result}, status_code=200)
    return JSONResponse(content={"message": "Cliente no encontrado"}, status_code=404)

@cliente_router.post("/clientes", tags=["Clientes"], response_model=Cliente)
def create_cliente(cliente: Cliente):
    """
    Crear un nuevo cliente.
    """
    db = SessionLocal()
    result = ClienteService(db).create_cliente(cliente)
    return JSONResponse(content={"cliente": result}, status_code=201)

@cliente_router.put("/clientes/{cliente_id}", tags=["Clientes"], response_model=Cliente)
def update_cliente(cliente_id: int, cliente: Cliente):
    """
    Actualizar un cliente existente.
    """
    db = SessionLocal()
    result = ClienteService(db).update_cliente(cliente_id, cliente)
    if result:
        return JSONResponse(content={"cliente": result}, status_code=200)
    return JSONResponse(content={"message": "Cliente no encontrado"}, status_code=404)

@cliente_router.delete("/clientes/{cliente_id}", tags=["Clientes"])
def delete_cliente(cliente_id: int):
    """
    Eliminar un cliente por su ID.
    """
    db = SessionLocal()
    success = ClienteService(db).delete_cliente(cliente_id)
    if success:
        return JSONResponse(content={"message": "Cliente eliminado"}, status_code=200)
    return JSONResponse(content={"message": "Cliente no encontrado"}, status_code=404)
