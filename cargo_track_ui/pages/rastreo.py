import streamlit as st
from api_client import get, APIError

ICONOS_ESTADO = {
    "PENDIENTE": "🕐",
    "EN_TRANSITO": "🚛",
    "ENTREGADO": "✅",
    "CANCELADO": "❌",
}


def mostrar():
    st.title("Rastreo de Envíos")

    if "ultimo_rastreo" not in st.session_state:
        st.session_state.ultimo_rastreo = None

    col_input, col_btn = st.columns([3, 1])
    envio_id = col_input.number_input(
        "Número de envío", min_value=1, step=1, label_visibility="collapsed"
    )
    buscar = col_btn.button("Rastrear", use_container_width=True)

    if buscar:
        st.session_state.ultimo_rastreo = int(envio_id)

    if st.session_state.ultimo_rastreo:
        _mostrar_rastreo(st.session_state.ultimo_rastreo)
        

def _mostrar_rastreo(envio_id: int):
    try:
        envio = get(f"/envios/{envio_id}")
    except APIError:
        st.error(f"No se encontró el envío #{envio_id}.")
        return
    except Exception:
        st.error("No se pudo conectar con el API.")
        return

    estado = envio["estado"]
    icono = ICONOS_ESTADO.get(estado, "📦")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader(f"Envío #{envio['id']}")
        st.write(f"**Origen:** {envio['origen']}")
        st.write(f"**Destino:** {envio['destino']}")
        st.write(f"**Peso:** {envio['peso']} kg")
        if envio.get("descripcion"):
            st.write(f"**Descripción:** {envio['descripcion']}")
    with col2:
        st.metric(label="Estado actual", value=f"{icono} {estado}")

    st.divider()
    st.subheader("Historial de estados")

    try:
        historial = get(f"/envios/{envio_id}/historial")
    except Exception:
        st.info("No hay historial disponible para este envío.")
        return

    if not historial:
        st.info("Este envío aún no tiene actualizaciones de estado registradas.")
        return

    for entrada in historial:
        est = entrada["estado"]
        fecha = entrada["fecha"][:19].replace("T", " ")
        icono_h = ICONOS_ESTADO.get(est, "📦")
        st.write(f"{icono_h} **{est}** — {fecha}")
        if entrada.get("nota"):
            st.caption(entrada["nota"])
