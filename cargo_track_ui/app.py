import streamlit as st

st.set_page_config(
    page_title="Cargo Track",
    page_icon="📦",
    layout="wide",
)

with st.sidebar:
    st.title("📦 Cargo Track")
    st.caption("Sistema de gestión logística")
    st.divider()

    pagina = st.radio(
        "Módulo",
        options=["Rastreo", "Envíos", "Clientes", "Conductores"],
        label_visibility="collapsed",
    )

if pagina == "Rastreo":
    from pages import rastreo
    rastreo.mostrar()
elif pagina == "Envíos":
    from pages import envios
    envios.mostrar()
elif pagina == "Clientes":
    from pages import clientes
    clientes.mostrar()
elif pagina == "Conductores":
    from pages import conductores
    conductores.mostrar()
