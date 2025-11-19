from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import SessionLocal, engine, Base
from routers.cliente import cliente_router
from routers.negocio import negocio_router
from routers.pedido import pedido_router
from routers.detalle_pedido import detalle_pedido_router
from routers.producto import producto_router
from routers.estadistica import estadistica_router
import sys
from pathlib import Path

# Agregar el directorio raíz al PYTHONPATH
sys.path.append(str(Path(__file__).resolve().parent))

app= FastAPI()
app.title="La poderosisima API de SalleVar"
app.version="0.0.1"

Base.metadata.create_all(bind=engine)

app.include_router(cliente_router)
app.include_router(negocio_router)
app.include_router(pedido_router)
app.include_router(detalle_pedido_router)
app.include_router(producto_router)
app.include_router(estadistica_router)

@app.get("/", tags=["Home"])
def read_root():
    return "Hola mundo"


