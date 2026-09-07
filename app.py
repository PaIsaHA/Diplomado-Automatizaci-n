import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Bootcamp Automatización", page_icon="⚙️", layout="wide", initial_sidebar_state="collapsed")

# --- ESTILOS CSS PERSONALIZADOS PARA DARLE "VIDA" Y OCULTAR INTERFAZ ---
st.markdown('''
<style>
    .main-title {
        font-size: 2.8rem !important;
        color: #ff4b4b;
        text-align: center;
        font-weight: 800;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1.3rem !important;
        color: #f0f2f6;
        text-align: center;
        margin-top: -10px;
        margin-bottom: 30px;
    }
    div[data-testid="metric-container"] {
        background-color: #262730;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.5);
    }
    
    /* Ocultar menú de Streamlit, footer y botón de perfil */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden !important;}
    [data-testid="stHeader"] {visibility: hidden !important;}
</style>
''', unsafe_allow_html=True)

# Encabezado principal con estilos
st.markdown("<h1 class='main-title'>⚙️ Bootcamp Intensivo en Automatización y Troubleshooting</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Centro de Innovación IECA + AAM Richard E. Dauch</p>", unsafe_allow_html=True)

# Layout de Introducción con columnas
col_intro1, col_intro2, col_intro3 = st.columns([2, 1, 1.2])

with col_intro1:
    st.info("**Objetivo Principal:** Desarrollar habilidades de troubleshooting (diagnóstico y solución de fallas reales) sin afectar la operatividad en piso, maximizando el uso de activos del CI.")
    st.markdown('''
    - 👨‍🎓 **Dirigido a:** Ganadores de HackAAMorphosis 2025, universitarios y académicos.
    - 🕒 **Horario:** Sábados de 08:00 a 14:00 hrs.
    - 📍 **Lugar:** Parque Industrial FIPASI, Silao, Guanajuato.
    ''')

with col_intro2:
    st.metric(label="Horas de Práctica/Teoría", value="72 hrs", delta="100% Aplicativo")

with col_intro3:
    st.metric(label="Especialidades", value="4 Módulos", delta="Troubleshooting Real")

st.divider()

# Sección de Temario y Gráfica Fusionada
st.header("📅 Cronograma y Módulos de Especialidad")

# Datos sin instructores
datos_modulos = [
    {"Módulo": "Entorno Allen Bradley", "Inicio": "2026-09-19", "Fin": "2026-10-03"},
    {"Módulo": "Entorno Siemens", "Inicio": "2026-10-10", "Fin": "2026-10-24"},
    {"Módulo": "Robótica Fanuc", "Inicio": "2026-10-31", "Fin": "2026-11-14"},
    {"Módulo": "Ecosistema Keyence", "Inicio": "2026-11-21", "Fin": "2026-12-05"}
]
df = pd.DataFrame(datos_modulos)
# Agregamos una columna de texto para que las fechas salgan dentro de la gráfica
df["Fechas"] = df["Inicio"] + " al " + df["Fin"]

# Gráfica de Gantt interactiva a pantalla completa
fig = px.timeline(df, x_start="Inicio", x_end="Fin", y="Módulo", text="Fechas", color="Módulo", 
                  color_discrete_sequence=px.colors.qualitative.Set2)
fig.update_yaxes(autorange="reversed")
fig.update_layout(margin=dict(l=0, r=0, t=20, b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", showlegend=False)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# Mapa y Registro en dos columnas
col_mapa, col_registro = st.columns([1, 1], gap="large")

with col_mapa:
    st.header("📍 Ubicación del Bootcamp")
    st.markdown("Encuéntranos en el **Instituto de Educación y Desarrollo Richard E. Dauch IECA - AAM**.")
    
    mapa_html = '''
    <iframe src="https://maps.google.com/maps?q=Instituto%20de%20Educaci%C3%B3n%20y%20Desarrollo%20Richard%20E.%20Dauch%20IECA%20-%20AAM%2C%20Silao%2C%20Gto.&t=&z=16&ie=UTF8&iwloc=&output=embed" width="100%" height="380" style="border:0; border-radius:15px; box-shadow: 0px 4px 10px rgba(0,0,0,0.3);" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
    '''
    components.html(mapa_html, height=400)

with col_registro:
    st.header("📝 Registro de Participantes")
    st.markdown("Llena los datos para apartar tu lugar.")
    with st.form("registro_form", clear_on_submit=True):
        nombre = st.text_input("Nombre Completo")
        correo = st.text_input("Correo Electrónico")
        procedencia = st.selectbox("Procedencia / Perfil", ["Ganador HackAAMorphosis 2025", "Universitario", "Académico", "Otro"])
        experiencia = st.text_area("Experiencia con automatización (opcional)")
        
        submit = st.form_submit_button("🚀 Enviar Registro", use_container_width=True)

        if submit:
            try:
                scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
                credenciales = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scopes)
                cliente = gspread.authorize(credenciales)
                
                fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                hoja = cliente.open("Registros").sheet1
                hoja.append_row([fecha_hora, nombre, correo, procedencia, experiencia])
                
                st.success(f"¡Registro exitoso para {nombre}! Datos guardados en la nube.")
            except Exception as e:
                st.error(f"Hubo un error de conexión: {e}")

# --- FOOTER / FIRMA DEL DESARROLLADOR ---
st.markdown("<br><hr><p style='text-align: center;'>Desarrollado en el Centro de Innovación IECA + AAM por <b>Ing. Pablo Horta</b></p>", unsafe_allow_html=True)
col_vacia1, col_logo, col_vacia2 = st.columns([4, 1, 4])
with col_logo:
    st.image("logo_ci.png", use_container_width=True)
