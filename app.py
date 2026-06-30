import streamlit as st
import pandas as pd
import datetime

st.set_page_config(layout="wide", page_title="Handball Tagger Pro")

# 1. Inicializar la memoria de datos y el estado visual de los botones
if 'eventos' not in st.session_state:
    st.session_state.eventos = []

estados_iniciales = {'Eq': 'LOC', 'Fase': 'Pos', 'Res': 'Gol', 'Err': 'N/A', 'Tipo': 'Lar'}
for k, v in estados_iniciales.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Función para cambiar el color del botón seleccionado sin recargar toda la página
def set_opcion(categoria, valor):
    st.session_state[categoria] = valor

st.title("Panel de Análisis Táctico")

modo = st.radio("Modo:", ["URL YouTube", "Video Local", "Tiempo Real"], horizontal=True)

col_video, col_datos = st.columns([1.5, 1])

with col_video:
    if modo == "URL YouTube":
        url = st.text_input("URL de YouTube:")
        if url:
            if "/live/" in url: url = url.replace("/live/", "/watch?v=")
            st.video(url)
    elif modo == "Video Local":
        archivo = st.file_uploader("Sube el video", type=["mp4"])
        if archivo: st.video(archivo)

    if len(st.session_state.eventos) > 0:
        df = pd.DataFrame(st.session_state.eventos)
        st.dataframe(df, height=200, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descargar CSV", data=csv, file_name='taggeo_partido.csv', mime='text/csv')

with col_datos:
    st.markdown("### Configuración de Equipos")
    c_loc, c_vis = st.columns(2)
    eq_loc = c_loc.text_input("Eq. Local (3 letras):", "LOC", max_chars=3).upper()
    eq_vis = c_vis.text_input("Eq. Visita (3 letras):", "VIS", max_chars=3).upper()

    st.markdown("### Selecciones (1 Toque)")
    
    # Motor para dibujar botones que se iluminan al tocarlos
    def dibujar_boton(label, categoria, valor_interno, col):
        activo = st.session_state[categoria] == valor_interno
        col.button(
            label, 
            type="primary" if activo else "secondary", 
            on_click=set_opcion, 
            args=(categoria, valor_interno),
            use_container_width=True,
            key=f"btn_{categoria}_{valor_interno}"
        )

    st.write("**Posesión**")
    c1, c2 = st.columns(2)
    dibujar_boton(eq_loc, 'Eq', eq_loc, c1)
    dibujar_boton(eq_vis, 'Eq', eq_vis, c2)

    st.write("**Fase y Resultado**")
    c1, c2, c3, c4 = st.columns(4)
    dibujar_boton("Pos", 'Fase', "Pos", c1)
    dibujar_boton("Tra", 'Fase', "Tra", c2)
    dibujar_boton("Gol", 'Res', "Gol", c3)
    dibujar_boton("No Gol", 'Res', "No Gol", c4)

    st.write("**Causa (Si es No Gol)**")
    c1, c2, c3, c4 = st.columns(4)
    dibujar_boton("N/A", 'Err', "N/A", c1)
    dibujar_boton("Per", 'Err', "Per", c2)
    dibujar_boton("Par", 'Err', "Par", c3)
    dibujar_boton("Fue", 'Err', "Fue", c4)

    st.write("**Tipo de Acción**")
    c1, c2, c3, c4, c5 = st.columns(5)
    dibujar_boton("Lar", 'Tipo', "Lar", c1)
    dibujar_boton("Ext", 'Tipo', "Ext", c2)
    dibujar_boton("Pen", 'Tipo', "Pen", c3)
    dibujar_boton("Pip", 'Tipo', "Pip", c4)
    dibujar_boton("Unf", 'Tipo', "Unf", c5)

    st.markdown("---")
    st.write("🥅 **Matriz de Portería (El toque registra la jugada)**")
    
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
    
    # Campo extra reubicado debajo de la portería
    extra = st.text_input("Extra (Dorsal / Notas):")
    
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

    # Lógica de registro que jala los datos del estado iluminado
    if zona_sel or btn_sin_tiro:
        nuevo = {
            "Time": datetime.datetime.now().strftime("%H:%M:%S"),
            "Eq": st.session_state.Eq,
            "Fase": st.session_state.Fase,
            "Res": st.session_state.Res,
            "Err": st.session_state.Err if st.session_state.Err != "N/A" else "",
            "Tipo": st.session_state.Tipo,
            "Zona": zona_sel if zona_sel else "N/A",
            "Extra": extra
        }
        st.session_state.eventos.append(nuevo)
        
        # Opcional: Reiniciar la casilla extra después de guardar para agilizar la siguiente jugada
        st.rerun()
