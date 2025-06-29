import streamlit as st
import pandas as pd
import numpy as np
import hashlib
import requests

# -------------------- Configuración inicial --------------------
st.set_page_config(page_title="Dashboard de Ventas", layout="wide")

# Usuarios válidos (con contraseñas hasheadas)
usuarios_validos = {
    "ana": hashlib.sha256("1234".encode()).hexdigest(),
    "carlos": hashlib.sha256("abc123".encode()).hexdigest(),
    "laura": hashlib.sha256("pass2024".encode()).hexdigest(),
}

# Inicializar sesión
if "logueado" not in st.session_state:
    st.session_state["logueado"] = False
if "usuario" not in st.session_state:
    st.session_state["usuario"] = ""
if "mensaje_logout" not in st.session_state:
    st.session_state["mensaje_logout"] = False

# -------------------- Funciones --------------------

def hash_clave(clave):
    return hashlib.sha256(clave.encode()).hexdigest()

def validar_usuario(usuario, clave):
    return usuario in usuarios_validos and usuarios_validos[usuario] == hash_clave(clave)

def login():
    st.title("🔐 Inicio de sesión")
    
    if st.session_state["mensaje_logout"]:
        st.success("✅ Has cerrado sesión correctamente.")
        st.session_state["mensaje_logout"] = False

    usuario = st.text_input("Usuario", placeholder="Escribe tu usuario")
    clave = st.text_input("Contraseña", type="password", placeholder="Escribe tu contraseña")
    
    if st.button("Ingresar"):
        if validar_usuario(usuario, clave):
            st.session_state["logueado"] = True
            st.session_state["usuario"] = usuario
            st.experimental_rerun()
        else:
            st.error("❌ Usuario o contraseña incorrectos.")

def consultar_api_agify(nombre):
    url = f"https://api.agify.io?name={nombre}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            st.error("⚠️ Error al consultar la API.")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error de conexión: {e}")
        return None

def dashboard():
    st.sidebar.title(f"👤 Usuario: {st.session_state['usuario']}")

    def cerrar_sesion():
        st.session_state["logueado"] = False
        st.session_state["usuario"] = ""
        st.session_state["mensaje_logout"] = True
        st.experimental_rerun()

    if st.sidebar.button("Cerrar sesión"):
        cerrar_sesion()

    st.title("📊 Dashboard de Ventas - Prueba de Concepto")

    # API
    with st.expander("🔍 Consulta de edad estimada por nombre"):
        nombre_input = st.text_input("Nombre:", key="nombre_api")
        if st.button("Consultar edad estimada"):
            if nombre_input.strip():
                resultado = consultar_api_agify(nombre_input.strip())
                if resultado:
                    st.info(
                        f"Nombre: **{resultado['name']}**\n\n"
                        f"Edad estimada: **{resultado['age']} años**\n\n"
                        f"Cantidad de datos: {resultado['count']}"
                    )
            else:
                st.warning("⚠️ Por favor, ingresa un nombre.")

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
    df_filtrado = df if categoria == "Todos" else df[df["Categoría"] == categoria]
    st.dataframe(df_filtrado, use_container_width=True)

    st.success("✔️ Dashboard funcional simulado.")

# -------------------- Ejecución principal --------------------

if not st.session_state["logueado"]:
    login()
else:
    dashboard()

