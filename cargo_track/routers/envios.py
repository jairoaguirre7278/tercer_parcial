from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..database import get_session
from ..models import Envio, Cliente
from ..schemas import EnvioCreate, EnvioRead, EnvioUpdate

router = APIRouter(prefix="/envios", tags=["Envíos"])


@router.get("/", response_model=list[EnvioRead])
def listar_envios(session: Session = Depends(get_session)):
    return session.exec(select(Envio)).all()


@router.get("/{envio_id}", response_model=EnvioRead)
def obtener_envio(envio_id: int, session: Session = Depends(get_session)):
    envio = session.get(Envio, envio_id)
    if not envio:
        raise HTTPException(status_code=404, detail="Envío no encontrado")
    return envio


@router.post("/", response_model=EnvioRead, status_code=201)
def crear_envio(envio: EnvioCreate, session: Session = Depends(get_session)):
    cliente = session.get(Cliente, envio.cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    db_envio = Envio.model_validate(envio)
    session.add(db_envio)
    session.commit()
    session.refresh(db_envio)
    return db_envio


@router.patch("/{envio_id}", response_model=EnvioRead)
def actualizar_envio(
    envio_id: int,
    datos: EnvioUpdate,
    session: Session = Depends(get_session),
):
    envio = session.get(Envio, envio_id)
    if not envio:
        raise HTTPException(status_code=404, detail="Envío no encontrado")
    datos_actualizados = datos.model_dump(exclude_unset=True)
    for campo, valor in datos_actualizados.items():
        setattr(envio, campo, valor)
    session.add(envio)
    session.commit()
    session.refresh(envio)
    return envio
