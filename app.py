import streamlit as st
import pandas as pd
import datetime

# Configuración para aprovechar toda la pantalla
st.set_page_config(layout="wide", page_title="Handball Tagger Pro")

if 'eventos' not in st.session_state:
    st.session_state.eventos = []

st.title("Panel de Análisis Táctico")

# 4. Selector de modos de análisis recuperado
modo = st.radio("Modo de Análisis:", ["URL YouTube", "Video Local", "Tiempo Real (Sin Video)"], horizontal=True)

# Distribución compacta para no tener que hacer scroll
col_video, col_datos = st.columns([1.5, 1])

with col_video:
    if modo == "URL YouTube":
        url = st.text_input("URL de YouTube:", placeholder="Pega el enlace aquí")
        if url:
            # 1. Corrección automática para enlaces de transmisiones en vivo (/live/)
            if "/live/" in url:
                url = url.replace("/live/", "/watch?v=")
            
            st.video(url)
            st.info("💡 **Controles de YouTube:** Usa el reproductor del video para Play/Pausa. Para 'Slow Motion', haz clic en el ícono de engranaje (⚙️) dentro del video y ajusta la 'Velocidad de reproducción'.")
            
    elif modo == "Video Local":
        archivo = st.file_uploader("Sube el video temporalmente (Solo para recortes)", type=["mp4"])
        if archivo:
            st.video(archivo)
            st.info("💡 **Controles Locales:** Usa el menú de 3 puntos (⋮) en la esquina del reproductor para ajustar la velocidad del video.")
            
    else:
        st.info("Modo Tiempo Real. Interfaz optimizada para captura rápida.")

    if len(st.session_state.eventos) > 0:
        df = pd.DataFrame(st.session_state.eventos)
        st.dataframe(df, height=150, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descargar CSV", data=csv, file_name='taggeo.csv', mime='text/csv')

with col_datos:
    st.markdown("### Registro Rápido")
    
    with st.form("registro_form", clear_on_submit=True):
        c_eq, c_fa, c_re = st.columns(3)
        with c_eq: equipo = st.radio("Eq", ["BER", "GUA"], horizontal=True)
        with c_fa: fase = st.radio("Fase", ["Pos", "Tra"], horizontal=True)
        with c_re: res = st.radio("Res", ["Gol", "No Gol"], horizontal=True)
        
        c_err, c_tip = st.columns(2)
        with c_err: error = st.radio("Err", ["N/A", "Per", "Par", "Fue"], horizontal=True)
        with c_tip: tipo = st.radio("Tipo", ["Lar", "Ext", "Pen", "Pip", "Unf"], horizontal=True)
        
        st.markdown("---")
        
        # 2. Selector de zona que NO envía el formulario automáticamente
        zona = st.selectbox("🥅 Zona de Portería:", [
            "N/A", 
            "Z1 (Sup-Izq ↖️)", "Z2 (Sup-Cen ⬆️)", "Z3 (Sup-Der ↗️)", 
            "Z4 (Med-Izq ⬅️)", "Z5 (Med-Cen ⏺️)", "Z6 (Med-Der ➡️)", 
            "Z7 (Inf-Izq ↙️)", "Z8 (Inf-Cen ⬇️)", "Z9 (Inf-Der ↘️)"
        ])
        
        st.markdown("---")
        
        # 3. Sección Extra recuperada para el número de jugadora
        extra = st.text_input("Extra (Jugadora/Notas):", placeholder="Ej. Dorsal 14")
        
        # 2. Botón principal destacado con un color diferente (type="primary")
        submit = st.form_submit_button("✅ REGISTRAR EVENTO", type="primary", use_container_width=True)

        if submit:
            nuevo = {
                "Time": datetime.datetime.now().strftime("%H:%M:%S"),
                "Eq": equipo,
                "Fase": fase,
                "Res": res,
                "Err": error if error != "N/A" else "",
                "Tipo": tipo,
                "Zona": zona[:2] if zona != "N/A" else "",
                "Extra": extra
            }
            st.session_state.eventos.append(nuevo)
            st.rerun()
