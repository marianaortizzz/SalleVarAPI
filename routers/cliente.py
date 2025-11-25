from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from config.database import SessionLocal
from schemas.cliente import Cliente
from schemas.LoginRequest import LoginRequest
from schemas.LoginResponse import LoginResponse
from schemas.UsuarioResponse import UsuarioResponse
from schemas.RepartidorResponse import RepartidorResponse
from services.cliente import ClienteService

cliente_router = APIRouter()

# Dependencia para obtener la sesión de la DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Obtener todos los clientes
@cliente_router.get("/clientes", tags=["Clientes"], response_model=List[Cliente])
def get_clientes(db: Session = Depends(get_db)):
    clientes = ClienteService(db).get_all()
    return clientes

# Obtener un cliente por ID
@cliente_router.get("/clientes/{cliente_id}", tags=["Clientes"], response_model=Cliente)
def get_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = ClienteService(db).get_by_id(cliente_id)
    if cliente:
        return cliente
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

# Crear un nuevo cliente
@cliente_router.post("/clientes", tags=["Clientes"], response_model=Cliente, status_code=201)
def create_cliente(cliente: Cliente, db: Session = Depends(get_db)):
    nuevo_cliente = ClienteService(db).create_cliente(cliente)
    return nuevo_cliente

# Actualizar un cliente existente
@cliente_router.put("/clientes/{cliente_id}", tags=["Clientes"], response_model=Cliente)
def update_cliente(cliente_id: int, cliente: Cliente, db: Session = Depends(get_db)):
    actualizado = ClienteService(db).update_cliente(cliente_id, cliente)
    if actualizado:
        return actualizado
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

# Eliminar un cliente por ID
@cliente_router.delete("/clientes/{cliente_id}", tags=["Clientes"])
def delete_cliente(cliente_id: int, db: Session = Depends(get_db)):
    success = ClienteService(db).delete_cliente(cliente_id)
    if success:
        return {"message": "Cliente eliminado"}
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

# LOGIN
@cliente_router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    service = ClienteService(db)
    usuario = service.login(data)

    if usuario is None:
        return LoginResponse(status_code=404, mensaje="Usuario no encontrado")

    if usuario is False:
        return LoginResponse(status_code=401, mensaje="Contraseña incorrecta")

    return LoginResponse(status_code=200, id_usuario=usuario.id_cliente, mensaje="Login exitoso")


# INFO USUARIO normal
@cliente_router.get("/mostrarInfoUsuario/{id_usuario}", response_model=UsuarioResponse)
def mostrar_info_usuario(id_usuario: int, db: Session = Depends(get_db)):
    service = ClienteService(db)
    cliente = service.get_by_id(id_usuario)

    if not cliente or cliente.repartidor:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return service.convert_to_usuario(cliente)


# INFO REPARTIDOR
@cliente_router.get("/obtenerInfoRepartidor/{id_usuario}", response_model=RepartidorResponse)
def obtener_info_repartidor(id_usuario: int, db: Session = Depends(get_db)):
    service = ClienteService(db)
    cliente = service.get_by_id(id_usuario)

    if not cliente or not cliente.repartidor:
        raise HTTPException(status_code=404, detail="Repartidor no encontrado")

    return service.convert_to_repartidor(cliente)

# 