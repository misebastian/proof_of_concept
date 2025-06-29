import streamlit as st
import pandas as pd
import numpy as np
import hashlib
import requests

# -------------------- Configuración inicial --------------------
st.set_page_config(page_title="Dashboard de Ventas", layout="wide")

# -------------------- Usuarios válidos --------------------
usuarios_validos = {
    "ana": hashlib.sha256("1234".encode()).hexdigest(),
    "carlos": hashlib.sha256("abc123".encode()).hexdigest(),
    "laura": hashlib.sha256("pass2024".encode()).hexdigest(),
}

# -------------------- Inicializar session_state --------------------
for key in ["logueado", "usuario", "pagina_actual"]:
    if key not in st.session_state:
        st.session_state[key] = False if key == "logueado" else ""

# -------------------- Funciones --------------------
def hash_clave(clave):
    return hashlib.sha256(clave.encode()).hexdigest()

def validar_usuario(usuario, clave):
    return usuario in usuarios_validos and usuarios_validos[usuario] == hash_clave(clave)

def login():
    st.title("🔐 Inicio de sesión")
    usuario = st.text_input("Usuario", key="usuario_input")
    clave = st.text_input("Contraseña", type="password", key="clave_input")
    if st.button("Ingresar"):
        if validar_usuario(usuario, clave):
            st.session_state["logueado"] = True
            st.session_state["usuario"] = usuario
            st.session_state["pagina_actual"] = "dashboard"
            st.experimental_rerun()
        else:
            st.error("❌ Usuario o contraseña incorrectos.")

def cerrar_sesion():
    st.session_state["logueado"] = False
    st.session_state["usuario"] = ""
    st.session_state["pagina_actual"] = "login"
    st.experimental_rerun()

def consultar_api_agify(nombre):
    try:
        response = requests.get(f"https://api.agify.io?name={nombre.strip()}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error("⚠️ Error al consultar la API.")
            return None
    except Exception as e:
        st.error(f"❌ Error de conexión: {e}")
        return None

def dashboard():
    st.sidebar.title(f"👤 Usuario: {st.session_state['usuario']}")
    st.sidebar.button("Cerrar sesión", on_click=cerrar_sesion)

    st.title("📊 Dashboard de Ventas - Prueba de Concepto")

    with st.expander("🔍 Consulta de edad estimada por nombre"):
        nombre_input = st.text_input("Nombre:", key="nombre_api")
        if st.button("Consultar edad estimada"):
            if nombre_input.strip():
                data = consultar_api_agify(nombre_input)
                if data:
                    st.info(
                        f"Nombre: **{data['name']}**\n\nEdad estimada: **{data['age']} años**\n\nDatos: {data['count']}")
            else:
                st.warning("⚠️ Escribe un nombre válido.")

    st.markdown("---")

    # KPIs
    col1, col2, col3 = st.columns(3)
    col1.metric("🛒 Ventas Totales", "$124,000", "+12%")
    col2.metric("👥 Clientes", "523", "+4")
    col3.metric("📦 Productos Vendidos", "1,370", "+9%")

    st.markdown("---")

    st.subheader("📈 Ventas mensuales")
    meses = pd.date_range("2024-01-01", periods=12, freq="M")
    ventas = np.random.randint(8000, 15000, size=12)
    df_ventas = pd.DataFrame({"Mes": meses, "Ventas": ventas})
    st.line_chart(df_ventas.set_index("Mes"))

    st.markdown("---")

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

# -------------------- Ejecución principal --------------------

if not st.session_state["logueado"] or st.session_state["pagina_actual"] == "login":
    login()
else:
    dashboard()

