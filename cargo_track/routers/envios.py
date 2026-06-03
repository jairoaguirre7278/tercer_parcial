from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..database import get_session
from ..models import Envio

router = APIRouter(prefix="/envios", tags=["Envíos"])


@router.get("/", response_model=list[Envio])
def listar_envios(session: Session = Depends(get_session)):
    return session.exec(select(Envio)).all()


@router.get("/{envio_id}", response_model=Envio)
def obtener_envio(envio_id: int, session: Session = Depends(get_session)):
    envio = session.get(Envio, envio_id)
    if not envio:
        raise HTTPException(status_code=404, detail="Envío no encontrado")
    return envio
