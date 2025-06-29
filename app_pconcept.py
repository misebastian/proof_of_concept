import streamlit as st
import pandas as pd
import numpy as np
import hashlib
import requests

# Configuración inicial
st.set_page_config(page_title="Dashboard de Ventas", layout="wide")

# Usuarios válidos
usuarios_validos = {
    "ana": hashlib.sha256("1234".encode()).hexdigest(),
    "carlos": hashlib.sha256("abc123".encode()).hexdigest(),
    "laura": hashlib.sha256("pass2024".encode()).hexdigest(),
}

# Estado de la sesión
if "pagina" not in st.session_state:
    st.session_state["pagina"] = "login"
if "usuario" not in st.session_state:
    st.session_state["usuario"] = ""

# Funciones
def hash_clave(clave):
    return hashlib.sha256(clave.encode()).hexdigest()

def validar_usuario(usuario, clave):
    return usuario in usuarios_validos and usuarios_validos[usuario] == hash_clave(clave)

def login():
    st.title("🔐 Inicio de sesión")
    usuario = st.text_input("Usuario")
    clave = st.text_input("Contraseña", type="password")
    if st.button("Ingresar"):
        if validar_usuario(usuario, clave):
            st.session_state["usuario"] = usuario
            st.session_state["pagina"] = "dashboard"
        else:
            st.error("❌ Usuario o contraseña incorrectos.")

def dashboard():
    st.sidebar.title(f"👤 Usuario: {st.session_state['usuario']}")
    if st.sidebar.button("Cerrar sesión"):
        st.session_state["usuario"] = ""
        st.session_state["pagina"] = "login"

    st.title("📊 Dashboard de Ventas - Prueba de Concepto")

    # API Agify
    with st.expander("🔍 Consulta de edad estimada por nombre"):
        nombre_input = st.text_input("Nombre:", key="nombre_api")
        if st.button("Consultar edad estimada"):
            if nombre_input.strip():
                try:
                    response = requests.get(f"https://api.agify.io?name={nombre_input.strip()}")
                    if response.status_code == 200:
                        data = response.json()
                        st.info(
                            f"Nombre: **{data['name']}**\n\nEdad estimada: **{data['age']} años**\n\nDatos: {data['count']}")
                    else:
                        st.error("❌ Error al consultar la API.")
                except Exception as e:
                    st.error(f"❌ Error de conexión: {e}")
            else:
                st.warning("⚠️ Escribe un nombre válido.")

    st.markdown("---")

    # KPIs
    col1, col2, col3 = st.columns(3)
    col1.metric("🛒 Ventas Totales", "$124,000", "+12%")
    col2.metric("👥 Clientes", "523", "+4")
    col3.metric("📦 Productos Vendidos", "1,370", "+9%")

    st.markdown("---")

    # Gráfico
    st.subheader("📈 Ventas mensuales")
    meses = pd.date_range("2024-01-01", periods=12, freq="M")
    ventas = np.random.randint(8000, 15000, size=12)
    df_ventas = pd.DataFrame({"Mes": meses, "Ventas": ventas})
    st.line_chart(df_ventas.set_index("Mes"))

    st.markdown("---")

    # Tabla filtrable
    st.subheader("📂 Detalle de ventas por producto")
    categoria = st.selectbox("Filtrar por categoría", ["Todos", "Tecnología", "Moda", "Hogar"])
    np.random.seed(42)
    data = {
        "Producto": [f"Producto {i}" for i in range(1, 21)],
        "Categoría": np.random.choice(["Tecnología", "Moda", "Hogar"], size=20),
        "Ventas ($)": np.random.randint(1000, 5000, size=20),
        "Unidades Vendidas": np.random.randint(10, 100, size=20),
    }
    df = pd.DataFrame(data)
    if categoria != "Todos":
        df = df[df["Categoría"] == categoria]
    st.dataframe(df, use_container_width=True)

    st.success("✔️ Dashboard funcional simulado.")

# Router principal
if st.session_state["pagina"] == "login":
    login()
elif st.session_state["pagina"] == "dashboard":
    dashboard()

