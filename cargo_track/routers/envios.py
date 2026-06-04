from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..database import get_session
from ..models import Envio, Cliente, EstadoEnvio
from ..schemas import EnvioCreate, EnvioRead, EnvioUpdate, CambioEstado
from ..auth import verificar_api_key

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
    

@router.delete("/{envio_id}", status_code=204)
def eliminar_envio(
    envio_id: int,
    session: Session = Depends(get_session),
    _: str = Depends(verificar_api_key),
):
    envio = session.get(Envio, envio_id)
    if not envio:
        raise HTTPException(status_code=404, detail="Envío no encontrado")
    session.delete(envio)
    session.commit()


TRANSICIONES_VALIDAS = {
    EstadoEnvio.PENDIENTE: [EstadoEnvio.EN_TRANSITO, EstadoEnvio.CANCELADO],
    EstadoEnvio.EN_TRANSITO: [EstadoEnvio.ENTREGADO, EstadoEnvio.CANCELADO],
    EstadoEnvio.ENTREGADO: [],
    EstadoEnvio.CANCELADO: [],
}


@router.patch("/{envio_id}/estado", response_model=EnvioRead)
def cambiar_estado(
    envio_id: int,
    cambio: CambioEstado,
    session: Session = Depends(get_session),
    _: str = Depends(verificar_api_key),
):
    envio = session.get(Envio, envio_id)
    if not envio:
        raise HTTPException(status_code=404, detail="Envío no encontrado")
    if cambio.estado not in TRANSICIONES_VALIDAS[envio.estado]:
        raise HTTPException(
            status_code=422,
            detail=f"No se puede cambiar de {envio.estado} a {cambio.estado}",
        )
    envio.estado = cambio.estado
    session.add(envio)
    session.commit()
    session.refresh(envio)
    return envio
