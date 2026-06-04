import httpx
import streamlit as st

BASE_URL = "http://127.0.0.1:8000"
USERNAME = "admin"
PASSWORD = "secret123"


class APIError(Exception):
    def __init__(self, status_code: int, mensaje: str):
        self.status_code = status_code
        self.mensaje = mensaje
        super().__init__(mensaje)


def _manejar_respuesta(response: httpx.Response):
    if response.status_code >= 400:
        try:
            detalle = response.json().get("detail", response.text)
        except Exception:
            detalle = response.text
        raise APIError(response.status_code, detalle)
    return response


def _obtener_token() -> str:
    if "access_token" not in st.session_state:
        response = httpx.post(
            f"{BASE_URL}/auth/token",
            data={"username": USERNAME, "password": PASSWORD},
        )
        _manejar_respuesta(response)
        st.session_state["access_token"] = response.json()["access_token"]
    return st.session_state["access_token"]


def _auth_headers() -> dict:
    return {"Authorization": f"Bearer {_obtener_token()}"}


def get(endpoint: str):
    response = httpx.get(f"{BASE_URL}{endpoint}")
    return _manejar_respuesta(response).json()


def post(endpoint: str, data: dict) -> dict:
    response = httpx.post(f"{BASE_URL}{endpoint}", json=data, headers=_auth_headers())
    return _manejar_respuesta(response).json()


def patch(endpoint: str, data: dict) -> dict:
    response = httpx.patch(f"{BASE_URL}{endpoint}", json=data, headers=_auth_headers())
    return _manejar_respuesta(response).json()


def delete(endpoint: str) -> None:
    response = httpx.delete(f"{BASE_URL}{endpoint}", headers=_auth_headers())
    _manejar_respuesta(response)
