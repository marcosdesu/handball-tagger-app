import streamlit as st
import pandas as pd
import datetime

st.set_page_config(layout="wide", page_title="Handball Tagger Pro")

if 'eventos' not in st.session_state:
    st.session_state.eventos = []

# Estado inicial
estados = {'Eq': 'LOC', 'Res': 'Gol', 'Fase': 'Pos', 'Err': 'N/A', 'Tipo': 'Lar', 'Lado': 'Cent'}
for k, v in estados.items():
    if k not in st.session_state: st.session_state[k] = v

def set_opcion(cat, val): st.session_state[cat] = val

st.title("Panel de Análisis Táctico")
modo = st.radio("Modo:", ["URL YouTube", "Video Local", "Tiempo Real"], horizontal=True)

col_video, col_datos = st.columns([1.5, 1])

with col_video:
    if modo == "URL YouTube":
        url = st.text_input("URL:")
        if url: 
            if "/live/" in url: url = url.replace("/live/", "/watch?v=")
            st.video(url)
    elif modo == "Video Local":
        archivo = st.file_uploader("Video:", type=["mp4"])
        if archivo: st.video(archivo)
    
    st.markdown("### Equipos")
    c_loc, c_vis = st.columns(2)
    eq_loc = c_loc.text_input("Local:", "LOC", max_chars=3).upper()
    eq_vis = c_vis.text_input("Visita:", "VIS", max_chars=3).upper()

    if len(st.session_state.eventos) > 0:
        df = pd.DataFrame(st.session_state.eventos)
        st.dataframe(df, height=200, use_container_width=True)
        st.download_button("📥 Descargar CSV", data=df.to_csv(index=False).encode('utf-8'), file_name='partido.csv', mime='text/csv')

with col_datos:
    def btn_g(lab, cat, val, col):
        col.button(lab, type="primary" if st.session_state[cat]==val else "secondary", 
                   on_click=set_opcion, args=(cat, val), use_container_width=True)

    st.write("**Equipo**"); c=st.columns(2); btn_g(eq_loc,'Eq',eq_loc,c[0]); btn_g(eq_vis,'Eq',eq_vis,c[1])
    st.write("**Resultado**"); c=st.columns(2); btn_g("Gol",'Res',"Gol",c[0]); btn_g("No gol",'Res',"No Gol",c[1])
    st.write("**Fase**"); c=st.columns(2); btn_g("Pos",'Fase',"Pos",c[0]); btn_g("Tra",'Fase',"Tra",c[1])
    st.write("**Error**"); c=st.columns(3); btn_g("Par",'Err',"Par",c[0]); btn_g("Per",'Err',"Per",c[1]); btn_g("Fue",'Err',"Fue",c[2])
    
    # Solución al IndexError: Dividido en 2 filas de 3
    st.write("**Tipo**")
    c1=st.columns(3); btn_g("Lar",'Tipo',"Lar",c1[0]); btn_g("Pen",'Tipo',"Pen",c1[1]); btn_g("Ext",'Tipo',"Ext",c1[2])
    c2=st.columns(3); btn_g("Piv",'Tipo',"Piv",c2[0]); btn_g("Unf",'Tipo',"Unf",c2[1]); btn_g("Dir",'Tipo',"Dir",c2[2])
    
    st.write("**Lado**"); c=st.columns(3); btn_g("Cent",'Lado',"Cent",c[0]); btn_g("Izq",'Lado',"Izq",c[1]); btn_g("Der",'Lado',"Der",c[2])
    
    extra = st.text_input("Extra:")
    
    st.markdown("---")
    st.write("🥅 **Matriz de Portería (Registra evento)**")
    z = st.columns(3); z1=z[0].button("Z1"); z2=z[1].button("Z2"); z3=z[2].button("Z3")
    z = st.columns(3); z4=z[0].button("Z4"); z5=z[1].button("Z5"); z6=z[2].button("Z6")
    z = st.columns(3); z7=z[0].button("Z7"); z8=z[1].button("Z8"); z9=z[2].button("Z9")
    btn_st = st.button("✅ REGISTRAR JUGADA", type="primary", use_container_width=True)

    zona_sel = next((f"Z{i}" for i, b in enumerate([z1,z2,z3,z4,z5,z6,z7,z8,z9], 1) if b), None)

    if zona_sel or btn_st:
        st.session_state.eventos.append({
            "Time": datetime.datetime.now().strftime("%H:%M:%S"),
            "Eq": st.session_state.Eq, "Res": st.session_state.Res, "Fase": st.session_state.Fase,
            "Err": st.session_state.Err if st.session_state.Err != "N/A" else "",
            "Tipo": st.session_state.Tipo, "Lado": st.session_state.Lado,
            "Zona": zona_sel if zona_sel else "N/A", "Extra": extra
        })
        st.rerun()
