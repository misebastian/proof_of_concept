import streamlit as st
import pandas as pd
import numpy as np

# Simulamos usuarios válidos
usuarios_validos = [
    {"usuario": "ana", "clave": "1234"},
    {"usuario": "carlos", "clave": "abc123"},
    {"usuario": "laura", "clave": "pass2024"},
]

# Sesión
if "logueado" not in st.session_state:
    st.session_state.logueado = False
if "usuario" not in st.session_state:
    st.session_state.usuario = ""

# Validar login
def validar_usuario(usuario, clave):
    for u in usuarios_validos:
        if u["usuario"] == usuario and u["clave"] == clave:
            return True
    return False

# LOGIN
if not st.session_state.logueado:
    st.title("🔐 Inicio de sesión")
    usuario_input = st.text_input("Usuario")
    clave_input = st.text_input("Contraseña", type="password")
    login_btn = st.button("Ingresar")

    if login_btn:
        if validar_usuario(usuario_input, clave_input):
            st.session_state.logueado = True
            st.session_state.usuario = usuario_input
            st.experimental_rerun()
        else:
            st.error("Usuario o contraseña incorrectos.")

# DASHBOARD
else:
    st.sidebar.title(f"👤 Usuario: {st.session_state.usuario}")
    st.sidebar.button("Cerrar sesión", on_click=lambda: (
        st.session_state.clear(), st.experimental_rerun()))

    st.title("📊 Dashboard de Ventas - Prueba de Concepto")

    # --- KPIs simulados
    col1, col2, col3 = st.columns(3)
    col1.metric("🛒 Ventas Totales", "$124,000", "+12%")
    col2.metric("👥 Clientes", "523", "+4")
    col3.metric("📦 Productos Vendidos", "1,370", "+9%")

    st.markdown("---")

    # --- Gráfico de ventas mensuales (simulado)
    st.subheader("📈 Ventas mensuales")
    meses = pd.date_range("2024-01-01", periods=12, freq="M")
    ventas = np.random.randint(8000, 15000, size=12)
    df_ventas = pd.DataFrame({"Mes": meses, "Ventas": ventas})
    st.line_chart(df_ventas.set_index("Mes"))

    # --- Filtro por categoría y tabla
    st.subheader("📂 Detalle de ventas por producto")
    categoria = st.selectbox("Filtrar por categoría", ["Todos", "Tecnología", "Moda", "Hogar"])

    # Datos simulados
    np.random.seed(42)
    data = {
        "Producto": [f"Producto {i}" for i in range(1, 21)],
        "Categoría": np.random.choice(["Tecnología", "Moda", "Hogar"], size=20),
        "Ventas": np.random.randint(1000, 5000, size=20),
        "Unidades": np.random.randint(10, 100, size=20),
    }
    df = pd.DataFrame(data)

    # Aplicar filtro
    if categoria != "Todos":
        df = df[df["Categoría"] == categoria]

    st.dataframe(df)

    st.success("✔️ Dashboard funcional simulado.")
