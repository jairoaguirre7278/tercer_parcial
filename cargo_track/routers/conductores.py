from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..database import get_session
from ..models import Conductor
from ..schemas import ConductorCreate, ConductorRead
from ..auth import verificar_api_key

router = APIRouter(prefix="/conductores", tags=["Conductores"])


@router.get("/", response_model=list[ConductorRead])
def listar_conductores(session: Session = Depends(get_session)):
    return session.exec(select(Conductor)).all()


@router.get("/{conductor_id}", response_model=ConductorRead)
def obtener_conductor(conductor_id: int, session: Session = Depends(get_session)):
    conductor = session.get(Conductor, conductor_id)
    if not conductor:
        raise HTTPException(status_code=404, detail="Conductor no encontrado")
    return conductor


@router.post("/", response_model=ConductorRead, status_code=201)
def crear_conductor(
    conductor: ConductorCreate,
    session: Session = Depends(get_session),
    _: str = Depends(verificar_api_key),
):
    db_conductor = Conductor.model_validate(conductor)
    session.add(db_conductor)
    session.commit()
    session.refresh(db_conductor)
    return db_conductor
