from contextlib import asynccontextmanager
from fastapi import FastAPI
from .database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="Cargo Track API",
    description="API para gestión de envíos logísticos",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def root():
    return {"mensaje": "Bienvenido a la API de Cargo Track"}
