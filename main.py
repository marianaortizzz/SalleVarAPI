from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import Session, engine, Base

app= FastAPI()
app.title="La poderosisima API de SalleVar"
app.version="0.0.1"

Base.metadata.create_all(bind=engine)


@app.get("/", tags=["Home"])
def read_root():
    return "Hola mundo"    


