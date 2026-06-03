from typing import Optional, List
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship


class EstadoEnvio(str, Enum):
    PENDIENTE = "PENDIENTE"
    EN_TRANSITO = "EN_TRANSITO"
    ENTREGADO = "ENTREGADO"
    CANCELADO = "CANCELADO"

class Cliente(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100)
    email: str = Field(unique=True, max_length=150)
    telefono: Optional[str] = Field(default=None, max_length=20)
    
    envios: List["Envio"] = Relationship(back_populates="cliente")


class Envio(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cliente_id: int = Field(foreign_key="cliente.id")
    origen: str = Field(max_length=100)
    destino: str = Field(max_length=100)
    peso: float
    descripcion: Optional[str] = Field(default=None)
    estado: EstadoEnvio = Field(default=EstadoEnvio.PENDIENTE)
    cliente_id: int = Field(foreign_key="cliente.id")
    cliente: Optional[Cliente] = Relationship(back_populates="envios")

class ConductorRuta(SQLModel, table=True):
    conductor_id: Optional[int] = Field(
        default=None, foreign_key="conductor.id", primary_key=True
    )
    ruta_id: Optional[int] = Field(
        default=None, foreign_key="ruta.id", primary_key=True
    )


class Conductor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100)
    licencia: str = Field(unique=True, max_length=50)
    email: str = Field(unique=True, max_length=150)

    rutas: List["Ruta"] = Relationship(
        back_populates="conductores", link_model=ConductorRuta
    )


class Ruta(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100)
    origen: str = Field(max_length=100)
    destino: str = Field(max_length=100)

    conductores: List[Conductor] = Relationship(
        back_populates="rutas", link_model=ConductorRuta
    )


class ConductorRuta(SQLModel, table=True):
    conductor_id: Optional[int] = Field(
        default=None, foreign_key="conductor.id", primary_key=True
    )
    ruta_id: Optional[int] = Field(
        default=None, foreign_key="ruta.id", primary_key=True
    )
