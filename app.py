import streamlit as st
import pandas as pd
import datetime

# Configuración ancha para aprovechar toda la pantalla
st.set_page_config(layout="wide", page_title="Handball Tagger Pro")

# Memoria de eventos
if 'eventos' not in st.session_state:
    st.session_state.eventos = []

st.title("Panel de Análisis Táctico")

# Distribución: 60% Video / Tabla | 40% Controles
col_video, col_datos = st.columns([1.5, 1])

with col_video:
    url = st.text_input("URL de YouTube (Video Oculto):", placeholder="https://youtu.be/...")
    if url:
        st.video(url)
    
    # La tabla de datos se dibuja justo debajo del video para monitorear sin hacer scroll
    if len(st.session_state.eventos) > 0:
        df = pd.DataFrame(st.session_state.eventos)
        st.dataframe(df, height=200, use_container_width=True)
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descargar CSV Tidy Data", data=csv, file_name='taggeo_partido.csv', mime='text/csv')

with col_datos:
    st.markdown("### Registro Rápido")
    
    with st.form("registro_form", clear_on_submit=True):
        
        # Botones de selección táctil en lugar de listas
        c_eq, c_fa, c_re = st.columns(3)
        with c_eq: equipo = st.radio("Equipo", ["BER", "GUA"], horizontal=True)
        with c_fa: fase = st.radio("Fase", ["Pos", "Tra"], horizontal=True)
        with c_re: res = st.radio("Resultado", ["Gol", "No Gol"], horizontal=True)
        
        c_err, c_tip = st.columns(2)
        with c_err: error = st.radio("Error", ["N/A", "Per", "Par", "Fue"], horizontal=True)
        with c_tip: tipo = st.radio("Tipo", ["Lar", "Ext", "Pen", "Pip", "Unf"], horizontal=True)
        
        st.markdown("---")
        st.write("🥅 **Portería (Toca la zona para Registrar)**")
        
        # Matriz 3x3: Cada botón funciona como el "Enter" para agilizar el proceso
        z_sup = st.columns(3)
        z1 = z_sup[0].form_submit_button("Z1 (Sup-Izq)", use_container_width=True)
        z2 = z_sup[1].form_submit_button("Z2 (Sup-Cen)", use_container_width=True)
        z3 = z_sup[2].form_submit_button("Z3 (Sup-Der)", use_container_width=True)
        
        z_med = st.columns(3)
        z4 = z_med[0].form_submit_button("Z4 (Med-Izq)", use_container_width=True)
        z5 = z_med[1].form_submit_button("Z5 (Med-Cen)", use_container_width=True)
        z6 = z_med[2].form_submit_button("Z6 (Med-Der)", use_container_width=True)
        
        z_inf = st.columns(3)
        z7 = z_inf[0].form_submit_button("Z7 (Inf-Izq)", use_container_width=True)
        z8 = z_inf[1].form_submit_button("Z8 (Inf-Cen)", use_container_width=True)
        z9 = z_inf[2].form_submit_button("Z9 (Inf-Der)", use_container_width=True)
        
        btn_sin_tiro = st.form_submit_button("Registrar Jugada (Sin Tiro)", use_container_width=True)

        # Lógica de guardado al presionar cualquier zona
        zona_sel = "N/A"
        if z1: zona_sel = "Z1"
        elif z2: zona_sel = "Z2"
        elif z3: zona_sel = "Z3"
        elif z4: zona_sel = "Z4"
        elif z5: zona_sel = "Z5"
        elif z6: zona_sel = "Z6"
        elif z7: zona_sel = "Z7"
        elif z8: zona_sel = "Z8"
        elif z9: zona_sel = "Z9"

        if any([z1, z2, z3, z4, z5, z6, z7, z8, z9, btn_sin_tiro]):
            nuevo = {
                "Time": datetime.datetime.now().strftime("%H:%M:%S"),
                "Eq": equipo,
                "Fase": fase,
                "Res": res,
                "Err": error if error != "N/A" else "",
                "Tipo": tipo,
                "Zona": zona_sel
            }
            st.session_state.eventos.append(nuevo)
            st.rerun() # Fuerza la actualización inmediata de la tabla
