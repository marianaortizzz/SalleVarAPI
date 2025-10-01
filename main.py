from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import Session, engine, Base
from routers.cliente import cliente_router
from routers.negocio import negocio_router

app= FastAPI()
app.title="La poderosisima API de SalleVar"
app.version="0.0.1"

Base.metadata.create_all(bind=engine)

app.include_router(cliente_router)
app.include_router(negocio_router)

@app.get("/", tags=["Home"])
def read_root():
    return "Hola mundo"    


