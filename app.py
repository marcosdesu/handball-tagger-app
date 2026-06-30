import streamlit as st
import pandas as pd
import datetime

st.set_page_config(layout="wide", page_title="Handball Tagger Pro")

if 'eventos' not in st.session_state:
    st.session_state.eventos = []

st.title("Panel de Análisis Táctico")

modo = st.radio("Modo:", ["URL YouTube", "Video Local", "Tiempo Real"], horizontal=True)

col_video, col_datos = st.columns([1.5, 1])

with col_video:
    if modo == "URL YouTube":
        url = st.text_input("URL de YouTube:")
        if url:
            if "/live/" in url: 
                url = url.replace("/live/", "/watch?v=")
            st.video(url)
            
    elif modo == "Video Local":
        archivo = st.file_uploader("Sube el video", type=["mp4"])
        if archivo:
            st.video(archivo)

    if len(st.session_state.eventos) > 0:
        df = pd.DataFrame(st.session_state.eventos)
        st.dataframe(df, height=200, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descargar CSV", data=csv, file_name='taggeo_partido.csv', mime='text/csv')

with col_datos:
    st.markdown("### Selecciones (1 Toque)")
    
    # Al eliminar st.form, cada clic se guarda en memoria automáticamente
    c_eq, c_fa = st.columns(2)
    with c_eq: equipo = st.radio("Eq", ["BER", "GUA"], horizontal=True)
    with c_fa: fase = st.radio("Fase", ["Pos", "Tra"], horizontal=True)
    
    c_re, c_err = st.columns(2)
    with c_re: res = st.radio("Res", ["Gol", "No Gol"], horizontal=True)
    with c_err: error = st.radio("Err", ["N/A", "Per", "Par", "Fue"], horizontal=True)
    
    tipo = st.radio("Tipo", ["Lar", "Ext", "Pen", "Pip", "Unf"], horizontal=True)
    
    extra = st.text_input("Extra (Jugadora/Notas):")
    
    st.markdown("---")
    st.write("🥅 **Matriz de Portería (El toque registra la jugada)**")
    
    # Botones independientes. Hacer clic en cualquiera ejecuta el registro.
    z_sup = st.columns(3)
    z1 = z_sup[0].button("Z1 ↖️", use_container_width=True)
    z2 = z_sup[1].button("Z2 ⬆️", use_container_width=True)
    z3 = z_sup[2].button("Z3 ↗️", use_container_width=True)
    
    z_med = st.columns(3)
    z4 = z_med[0].button("Z4 ⬅️", use_container_width=True)
    z5 = z_med[1].button("Z5 ⏺️", use_container_width=True)
    z6 = z_med[2].button("Z6 ➡️", use_container_width=True)
    
    z_inf = st.columns(3)
    z7 = z_inf[0].button("Z7 ↙️", use_container_width=True)
    z8 = z_inf[1].button("Z8 ⬇️", use_container_width=True)
    z9 = z_inf[2].button("Z9 ↘️", use_container_width=True)
    
    btn_sin_tiro = st.button("✅ Registrar Jugada (Sin Tiro)", type="primary", use_container_width=True)

    zona_sel = None
    if z1: zona_sel = "Z1"
    elif z2: zona_sel = "Z2"
    elif z3: zona_sel = "Z3"
    elif z4: zona_sel = "Z4"
    elif z5: zona_sel = "Z5"
    elif z6: zona_sel = "Z6"
    elif z7: zona_sel = "Z7"
    elif z8: zona_sel = "Z8"
    elif z9: zona_sel = "Z9"

    if zona_sel or btn_sin_tiro:
        nuevo = {
            "Time": datetime.datetime.now().strftime("%H:%M:%S"),
            "Eq": equipo,
            "Fase": fase,
            "Res": res,
            "Err": error if error != "N/A" else "",
            "Tipo": tipo,
            "Zona": zona_sel if zona_sel else "N/A",
            "Extra": extra
        }
        st.session_state.eventos.append(nuevo)
        st.rerun()
