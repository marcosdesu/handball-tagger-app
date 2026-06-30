import streamlit as st
import pandas as pd
import datetime

# 1. Configuración de la página
st.set_page_config(layout="wide", page_title="Handball Analytics Pro")

# 2. Inicializar la "memoria" de la app para guardar los datos
if 'eventos' not in st.session_state:
    st.session_state.eventos = []

st.title("Panel de Tagueo - Selección Femenil")

modo = st.radio("Modo de Análisis:", ["Video Local", "URL YouTube", "Tiempo Real (Sin Video)"], horizontal=True)

col_video, col_datos = st.columns([2, 1])

# --- SECCIÓN DE VIDEO ---
with col_video:
    if modo == "URL YouTube":
        url = st.text_input("Pega la URL de YouTube:")
        if url:
            st.video(url)
    elif modo == "Video Local":
        archivo = st.file_uploader("Sube el video", type=["mp4"])
        if archivo:
            st.video(archivo)
    else:
        st.info("Modo Tiempo Real Activo. Ojos en la pista, registra solo lo esencial.")
        
    # Mostrar la tabla de datos en vivo debajo del video
    if len(st.session_state.eventos) > 0:
        st.markdown("### 📊 Base de Datos del Partido")
        df = pd.DataFrame(st.session_state.eventos)
        st.dataframe(df, use_container_width=True)
        
        # Botón para descargar el CSV Tidy Data
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar CSV para Análisis",
            data=csv,
            file_name=f'handball_data_{datetime.datetime.now().strftime("%Y%m%d")}.csv',
            mime='text/csv',
        )

# --- SECCIÓN DE TAGUEO ---
with col_datos:
    st.subheader("Registro de Acción")
    
    with st.form("registro_form", clear_on_submit=True):
        col_eq, col_fase = st.columns(2)
        with col_eq:
            equipo = st.selectbox("Equipo", ["MÉXICO", "RIVAL"])
        with col_fase:
            fase = st.selectbox("Fase", ["Posicional (Pos)", "Transición (Tra)"])
            
        resultado = st.radio("Resultado", ["Gol", "No Gol (Fallo/Pérdida)"], horizontal=True)
        
        causa_error = st.selectbox("Causa (Si es No Gol)", ["N/A", "Pérdida (Per)", "Parada (Par)", "Fuera/Blocaje (Fue)"])
        tipo_lanzamiento = st.selectbox("Tipo/Error", ["Larga Distancia (Lar)", "Extremo (Ext)", "Penetración (Pen)", "Pivote (Pip)", "No Forzado (Unf)"])
        
        st.markdown("---")
        st.write("📍 **Matriz de Portería (3x3)**")
        zona = st.selectbox(
            "Zona del Lanzamiento", 
            ["N/A", 
             "Z1 (Sup-Izq)", "Z2 (Sup-Cen)", "Z3 (Sup-Der)", 
             "Z4 (Med-Izq)", "Z5 (Med-Cen)", "Z6 (Med-Der)", 
             "Z7 (Inf-Izq)", "Z8 (Inf-Cen)", "Z9 (Inf-Der)"]
        )
        
        st.markdown("---")
        dorsal = st.text_input("Dorsal Jugadora (Opcional):", placeholder="Ej. 14")
        
        submit = st.form_submit_button("Registrar Evento", use_container_width=True)
        
        # Lógica al presionar el botón
        if submit:
            nuevo_evento = {
                "Timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
                "Equipo": equipo,
                "Fase": fase[:3], # Guarda solo Pos o Tra
                "Resultado": "Gol" if "Gol" in resultado and "No Gol" not in resultado else "No Gol",
                "Causa_No_Gol": causa_error[:3] if causa_error != "N/A" else "",
                "Tipo_Lanzamiento": tipo_lanzamiento[:3],
                "Zona": zona[:2] if zona != "N/A" else "",
                "Jugadora": dorsal if dorsal else ""
            }
            # Agregar el evento a la memoria
            st.session_state.eventos.append(nuevo_evento)
            st.success("✅ Jugada registrada en la base de datos.")
