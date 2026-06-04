import streamlit as st
from api_client import get, post, patch, delete, APIError


COLORES_ESTADO = {
    "PENDIENTE": "🟡",
    "EN_TRANSITO": "🔵",
    "ENTREGADO": "🟢",
    "CANCELADO": "🔴",
}


def _badge_estado(estado: str) -> str:
    return f"{COLORES_ESTADO.get(estado, '⚪')} {estado}"

def mostrar():
    st.title("Gestión de Envíos")

    try:
        todos = get("/envios/")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total", len(todos))
        col2.metric("Pendientes", sum(1 for e in todos if e["estado"] == "PENDIENTE"))
        col3.metric("En tránsito", sum(1 for e in todos if e["estado"] == "EN_TRANSITO"))
        col4.metric("Entregados", sum(1 for e in todos if e["estado"] == "ENTREGADO"))
    except Exception:
        pass

    tab_lista, tab_crear, tab_estado = st.tabs(
        ["Ver envíos", "Nuevo envío", "Cambiar estado"]
    )

    with tab_lista:
        _tab_lista()
    with tab_crear:
        _tab_crear()
    with tab_estado:
        _tab_cambiar_estado()


def _tab_lista():
    col_titulo, col_reload = st.columns([4, 1])
    col_titulo.subheader("Envíos registrados")
    if col_reload.button("Actualizar", use_container_width=True):
        st.rerun()
        
    st.subheader("Envíos registrados")

    filtro = st.selectbox(
        "Filtrar por estado",
        options=["Todos", "PENDIENTE", "EN_TRANSITO", "ENTREGADO", "CANCELADO"],
    )

    with st.spinner("Cargando envíos..."):
        try:
            envios = get("/envios/")
        except APIError as e:
            st.error(f"Error {e.status_code}: {e.mensaje}")
            return
        except Exception:
            st.error("No se pudo conectar con el API. Verifica que el servidor esté corriendo.")
            return

    if filtro != "Todos":
        envios = [e for e in envios if e["estado"] == filtro]

    if not envios:
        st.info("No hay envíos que mostrar.")
        return

    st.dataframe(
        envios,
        column_config={
            "id": "ID",
            "cliente_id": "Cliente ID",
            "origen": "Origen",
            "destino": "Destino",
            "peso": st.column_config.NumberColumn("Peso (kg)", format="%.1f kg"),
            "estado": "Estado",
            "descripcion": "Descripción",
        },
        use_container_width=True,
        hide_index=True,
    )
    st.divider()
    with st.expander("Eliminar un envío"):
        envio_id_del = st.number_input(
            "ID del envío a eliminar", min_value=1, step=1, key="del_id"
        )
        confirmar = st.checkbox("Confirmo que quiero eliminar este envío")
        if st.button("Eliminar", disabled=not confirmar, type="primary"):
            try:
                delete(f"/envios/{int(envio_id_del)}")
                st.success(f"Envío #{int(envio_id_del)} eliminado.")
                st.rerun()
            except APIError as e:
                st.error(f"Error {e.status_code}: {e.mensaje}")


def _tab_crear():
    st.subheader("Registrar nuevo envío")

    try:
        clientes = get("/clientes/")
        if not clientes:
            st.warning("No hay clientes registrados. Crea uno primero en el módulo de Clientes.")
            return
        opciones_clientes = {f"{c['nombre']} (ID: {c['id']})": c["id"] for c in clientes}
    except Exception as e:
        st.error(f"No se pudo cargar la lista de clientes: {e}")
        return

    with st.form("form_crear_envio"):
        cliente_sel = st.selectbox("Cliente", options=list(opciones_clientes.keys()))
        col1, col2 = st.columns(2)
        origen = col1.text_input("Ciudad de origen")
        destino = col2.text_input("Ciudad de destino")
        peso = st.number_input("Peso (kg)", min_value=0.1, step=0.1, value=1.0)
        descripcion = st.text_area("Descripción (opcional)", height=80)
        enviado = st.form_submit_button("Crear envío", use_container_width=True)

    if enviado:
        if not origen or not destino:
            st.warning("Por favor completa origen y destino.")
            return
        try:
            nuevo = post("/envios/", {
                "cliente_id": opciones_clientes[cliente_sel],
                "origen": origen,
                "destino": destino,
                "peso": peso,
                "descripcion": descripcion or None,
            })
            st.success(f"Envío #{nuevo['id']} creado exitosamente. Estado: {nuevo['estado']}")
            st.balloons()
        except APIError as e:
            st.error(f"Error {e.status_code}: {e.mensaje}")
        except Exception:
            st.error("No se pudo conectar con el API.")


def _tab_cambiar_estado():
    st.subheader("Actualizar estado de un envío")

    envio_id = st.number_input("ID del envío", min_value=1, step=1)
    nuevo_estado = st.selectbox(
        "Nuevo estado",
        options=["EN_TRANSITO", "ENTREGADO", "CANCELADO"],
    )

    if st.button("Actualizar estado", use_container_width=True):
        try:
            actualizado = patch(f"/envios/{int(envio_id)}/estado", {"estado": nuevo_estado})
            st.success(f"Estado actualizado a: {actualizado['estado']}")
        except APIError as e:
            st.error(f"Error {e.status_code}: {e.mensaje}")
        except Exception:
            st.error("No se pudo conectar con el API.")
