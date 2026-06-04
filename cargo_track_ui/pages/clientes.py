import streamlit as st
from api_client import get, post, APIError


def mostrar():
    st.title("Gestión de Clientes")

    tab_lista, tab_crear = st.tabs(["Ver clientes", "Nuevo cliente"])

    with tab_lista:
        _tab_lista()
    with tab_crear:
        _tab_crear()


def _tab_lista():
    st.subheader("Clientes registrados")

    with st.spinner("Cargando clientes..."):
        try:
            clientes = get("/clientes/")
        except APIError as e:
            st.error(f"Error {e.status_code}: {e.mensaje}")
            return
        except Exception:
            st.error("No se pudo conectar con el API.")
            return

    if not clientes:
        st.info("No hay clientes registrados.")
        return

    st.dataframe(
        clientes,
        column_config={
            "id": "ID",
            "nombre": "Nombre",
            "email": "Correo",
            "telefono": "Teléfono",
        },
        use_container_width=True,
        hide_index=True,
    )


def _tab_crear():
    st.subheader("Registrar nuevo cliente")

    with st.form("form_crear_cliente"):
        nombre = st.text_input("Nombre completo")
        email = st.text_input("Correo electrónico")
        telefono = st.text_input("Teléfono (opcional)")
        enviado = st.form_submit_button("Registrar cliente", use_container_width=True)

    if enviado:
        if not nombre or not email:
            st.warning("El nombre y el correo son obligatorios.")
            return
        try:
            nuevo = post("/clientes/", {
                "nombre": nombre,
                "email": email,
                "telefono": telefono or None,
            })
            st.success(f"Cliente '{nuevo['nombre']}' registrado con ID #{nuevo['id']}.")
        except APIError as e:
            st.error(f"Error {e.status_code}: {e.mensaje}")
        except Exception:
            st.error("No se pudo conectar con el API.")
