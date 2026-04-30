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
        "Albañilería", "Fontanería", "Electricidad", 
        "Pintura", "Estructura", "Limpieza", "Otros"
    ])
    
    avance = st.select_slider(
        "Porcentaje de avance de la obra",
        options=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
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

    # --- ENVIAR POR CORREO (Configuración) ---
    st.markdown("---")
    st.subheader("Enviar informe por Email")
    email_destino = st.text_input("Correo electrónico del receptor")
    
    if st.button("📧 Enviar por Correo"):
        # NOTA: Para que esto funcione en la nube, necesitas configurar 
        # SMTP (ej. Gmail) y usar "Secrets" en Streamlit para la contraseña.
        st.warning("La función de envío requiere configuración de servidor SMTP.")
        # Aquí iría la lógica de smtplib (ver explicación abajo)
