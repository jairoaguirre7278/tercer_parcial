import streamlit as st
from api_client import get, post, APIError


def mostrar():
    st.title("Gestión de Conductores")

    tab_lista, tab_crear = st.tabs(["Ver conductores", "Nuevo conductor"])

    with tab_lista:
        _tab_lista()
    with tab_crear:
        _tab_crear()


def _tab_lista():
    st.subheader("Conductores registrados")

    with st.spinner("Cargando conductores..."):
        try:
            conductores = get("/conductores/")
        except APIError as e:
            st.error(f"Error {e.status_code}: {e.mensaje}")
            return
        except Exception:
            st.error("No se pudo conectar con el API.")
            return

    if not conductores:
        st.info("No hay conductores registrados.")
        return

    st.dataframe(
        conductores,
        column_config={
            "id": "ID",
            "nombre": "Nombre",
            "licencia": "Licencia",
            "email": "Correo",
        },
        use_container_width=True,
        hide_index=True,
    )


def _tab_crear():
    st.subheader("Registrar nuevo conductor")

    with st.form("form_crear_conductor"):
        nombre = st.text_input("Nombre completo")
        licencia = st.text_input("Número de licencia")
        email = st.text_input("Correo electrónico")
        enviado = st.form_submit_button("Registrar conductor", use_container_width=True)

    if enviado:
        if not nombre or not licencia or not email:
            st.warning("Todos los campos son obligatorios.")
            return
        try:
            nuevo = post("/conductores/", {
                "nombre": nombre,
                "licencia": licencia,
                "email": email,
            })
            st.success(f"Conductor '{nuevo['nombre']}' registrado con ID #{nuevo['id']}.")
        except APIError as e:
            st.error(f"Error {e.status_code}: {e.mensaje}")
        except Exception:
            st.error("No se pudo conectar con el API.")
