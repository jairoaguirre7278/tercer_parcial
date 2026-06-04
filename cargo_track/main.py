from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from .database import create_db_and_tables
from .routers import envios, clientes, conductores, auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


tags_metadata = [
    {
        "name": "Envíos",
        "description": "Gestión de envíos: crear, consultar, actualizar estado y eliminar.",
    },
    {
        "name": "Clientes",
        "description": "Registro y consulta de clientes del sistema Cargo Track.",
    },
    {
        "name": "Conductores",
        "description": "Registro y consulta de conductores.",
    },
]


app = FastAPI(
    title="Cargo Track API",
    description="API REST para gestión de envíos logísticos de Cargo Track",
    version="1.0.0",
    lifespan=lifespan,
    openapi_tags=tags_metadata,
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "codigo": 422,
            "mensaje": "Error de validación en los datos enviados",
            "detalle": str(exc.errors()),
        },
    )


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "codigo": 404,
            "mensaje": "El recurso solicitado no existe",
            "detalle": str(request.url),
        },
    )


@app.exception_handler(500)
async def server_error_handler(request: Request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "codigo": 500,
            "mensaje": "Error interno del servidor",
            "detalle": None,
        },
    )


app.include_router(auth.router)
app.include_router(clientes.router)
app.include_router(envios.router)
app.include_router(conductores.router)

@app.get("/")
def root():
    return {"mensaje": "Bienvenido a la API de Cargo Track"}
