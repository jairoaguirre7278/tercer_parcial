from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ..auth import USUARIOS, verificar_password, crear_token

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    usuario = USUARIOS.get(form_data.username)
    if not usuario or not verificar_password(form_data.password, usuario["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = crear_token(data={"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}
