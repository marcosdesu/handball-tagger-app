import streamlit as st
import pandas as pd
import time

st.set_page_config(layout="wide", page_title="Handball Tagger Pro")

# Inicialización
if 'eventos' not in st.session_state: st.session_state.eventos = []
if 'cronometro' not in st.session_state: st.session_state.cronometro = 0
if 'corriendo' not in st.session_state: st.session_state.corriendo = False

# Estado inicial de botones
estados = {'Eq': None, 'Res': None, 'Fase': None, 'Err': None, 'Tipo': None, 'Lado': None, 'Zona': None}
for k, v in estados.items():
    if k not in st.session_state: st.session_state[k] = v

def set_opcion(cat, val): st.session_state[cat] = val

st.title("Panel de Análisis Táctico")

# Control de Tiempo
c_vid, c_dat = st.columns([1.5, 1])

with c_vid:
    # Lógica de cronómetro en vivo
    c_time = st.columns([1, 3])
    if c_time[0].button("▶️ Iniciar/Pausar"): st.session_state.corriendo = not st.session_state.corriendo
    c_time[1].write(f"### Cronómetro: {st.session_state.cronometro}s")
    if st.session_state.corriendo:
        time.sleep(1)
        st.session_state.cronometro += 1
        st.rerun()

with c_dat:
    # 1. Configuración Equipos
    c_loc, c_vis = st.columns(2)
    eq_loc = c_loc.text_input("Local:", "LOC", max_chars=3).upper()
    eq_vis = c_vis.text_input("Visita:", "VIS", max_chars=3).upper()

    def btn_g(lab, cat, val, col):
        col.button(lab, type="primary" if st.session_state[cat]==val else "secondary", 
                   on_click=set_opcion, args=(cat, val), use_container_width=True)

    # 2. Orden estricto con lógica de un solo toque
    st.write("**Equipo**"); c=st.columns(2); btn_g(eq_loc,'Eq',eq_loc,c[0]); btn_g(eq_vis,'Eq',eq_vis,c[1])
    st.write("**Resultado**"); c=st.columns(2); btn_g("Gol",'Res',"Gol",c[0]); btn_g("No gol",'Res',"No Gol",c[1])
    st.write("**Fase**"); c=st.columns(2); btn_g("Pos",'Fase',"Pos",c[0]); btn_g("Tra",'Fase',"Tra",c[1])
    st.write("**Error**"); c=st.columns(3); btn_g("Par",'Err',"Par",c[0]); btn_g("Per",'Err',"Per",c[1]); btn_g("Fue",'Err',"Fue",c[2])
    st.write("**Tipo**"); c1=st.columns(3); btn_g("Lar",'Tipo',"Lar",c1[0]); btn_g("Pen",'Tipo',"Pen",c1[1]); btn_g("Ext",'Tipo',"Ext",c1[2])
    c2=st.columns(3); btn_g("Piv",'Tipo',"Piv",c2[0]); btn_g("Unf",'Tipo',"Unf",c2[1]); btn_g("Dir",'Tipo',"Dir",c2[2])
    st.write("**Lado**"); c=st.columns(3); btn_g("Cent",'Lado',"Cent",c[0]); btn_g("Izq",'Lado',"Izq",c[1]); btn_g("Der",'Lado',"Der",c[2])
    
    st.write("**Zona Portería**")
    # Aumentamos el tamaño de los botones usando menos columnas (2 por fila en vez de 3)
    z_row1 = st.columns(2); btn_g("Z1-Z2",'Zona',"Z1-Z2",z_row1[0]); btn_g("Z3",'Zona',"Z3",z_row1[1])
    z_row2 = st.columns(2); btn_g("Z4-Z5",'Zona',"Z4-Z5",z_row2[0]); btn_g("Z6",'Zona',"Z6",z_row2[1])
    z_row3 = st.columns(2); btn_g("Z7-Z8",'Zona',"Z7-Z8",z_row3[0]); btn_g("Z9",'Zona',"Z9",z_row3[1])
    
    extra = st.text_input("Extra:")
    
    # 3. Registro Manual Único
    if st.button("✅ REGISTRAR JUGADA", type="primary", use_container_width=True):
        st.session_state.eventos.append({
            "Time": st.session_state.cronometro,
            "Eq": st.session_state.Eq, "Res": st.session_state.Res, "Fase": st.session_state.Fase,
            "Err": st.session_state.Err if st.session_state.Err != "N/A" else "",
            "Tipo": st.session_state.Tipo, "Lado": st.session_state.Lado,
            "Zona": st.session_state.Zona, "Extra": extra
        })
        # Resetear estado a predeterminado
        for k in estados: st.session_state[k] = estados[k]
        st.rerun()
