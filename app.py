import streamlit as st
import pandas as pd
from io import BytesIO
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import date

# Configuración de página
st.set_page_config(page_title="Seguimiento de Obra", layout="centered")

# --- PORTADA Y LOGO ---
# Reemplaza 'logo.png' con la ruta de tu imagen
try:
    st.image("6b07cb19-ba91-479a-a646-7c1a2663c633.jpg", width=200)
except:
    st.title("🏗️ Seguimiento de Obra")

st.markdown("### Reporte Diario de Actividad")

# --- FORMULARIO ---
with st.form("formulario_obra"):
    nombre = st.text_input("Nombre del Trabajador")
    
    funcion = st.selectbox("Función realizada", [
        "Trazado y marcado de cajas, tubos y cuadros", "Ejecución rozas en paredes y techos", "Montaje de soportes", 
        "Colocación tubos y conductos", "Tendido de cables", "Identificación y etiquetado", "Conexionado de cables en bornes o regletas", "Instalación y conexionado de mecanismos", "Fijación de carril DIN y mecanismos en cuadro eléctrico", "Cableado interno del cuadro eléctrico", "Configuración de equipos domóticos y/o automáticos", "Conexionado de sensores/actuadores de equipos domóticos/automáticos", "Pruebas de continuidad", "Pruebas de aislamiento", "Verificación de tierras", "Programación del automatismo", "Pruebas de funcionamiento"
    ])
    
    avance = st.select_slider(
        "Porcentaje de avance de la obra",
        options=[0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100],
        value=0
    )
    
    comentarios = st.text_area("Comentarios y observaciones")
    fecha = st.date_input("Fecha del reporte", date.today())
    
    submitted = st.form_submit_button("Registrar Datos")

# --- GESTIÓN DE DATOS ---
if "datos_reporte" not in st.session_state:
    st.session_state.datos_reporte = []

if submitted:
    nuevo_registro = {
        "Fecha": fecha,
        "Trabajador": nombre,
        "Función": funcion,
        "Avance %": avance,
        "Comentarios": comentarios
    }
    st.session_state.datos_reporte.append(nuevo_registro)
    st.success("✅ Datos registrados localmente")

# Mostrar tabla previa
if st.session_state.datos_reporte:
    df = pd.DataFrame(st.session_state.datos_reporte)
    st.write("### Vista previa del informe")
    st.dataframe(df)

    # --- GENERAR EXCEL ---
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Reporte')
    excel_data = output.getvalue()

    st.download_button(
        label="📥 Descargar Excel",
        data=excel_data,
        file_name=f"reporte_obra_{fecha}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
