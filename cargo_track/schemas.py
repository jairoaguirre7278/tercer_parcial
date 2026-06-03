from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator
from .models import EstadoEnvio


class ClienteCreate(BaseModel):
    nombre: str
    email: EmailStr
    telefono: Optional[str] = None


class ClienteRead(BaseModel):
    id: int
    nombre: str
    email: str
    telefono: Optional[str]

    model_config = {"from_attributes": True}


class EnvioCreate(BaseModel):
    cliente_id: int
    origen: str
    destino: str
    peso: float
    descripcion: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "cliente_id": 1,
                "origen": "Bogotá",
                "destino": "Medellín",
                "peso": 5.5,
                "descripcion": "Documentos urgentes",
            }
        }
    }

    @field_validator("peso")
    @classmethod
    def peso_positivo(cls, v):
        if v <= 0:
            raise ValueError("El peso debe ser mayor que cero")
        return v


class EnvioRead(BaseModel):
    id: int
    cliente_id: int
    origen: str
    destino: str
    peso: float
    descripcion: Optional[str]
    estado: EstadoEnvio

    model_config = {"from_attributes": True}


class EnvioUpdate(BaseModel):
    origen: Optional[str] = None
    destino: Optional[str] = None
    peso: Optional[float] = None
    descripcion: Optional[str] = None
