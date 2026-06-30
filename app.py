import streamlit as st
import pandas as pd
import time

st.set_page_config(layout="wide", page_title="Handball Live Pro")

if 'eventos' not in st.session_state: st.session_state.eventos = []
if 'tiempo' not in st.session_state: st.session_state.tiempo = 0
if 'corriendo' not in st.session_state: st.session_state.corriendo = False

estados = {'Eq': 'LOC', 'Res': 'Gol', 'Fase': 'Pos', 'Err': 'N/A', 'Tipo': 'Lar', 'Lado': 'Cent', 'Zona': 'N/A'}
for k, v in estados.items():
    if k not in st.session_state: st.session_state[k] = v

def set_opcion(cat, val): st.session_state[cat] = val

st.title("Panel de Análisis Táctico")

# --- DISTRIBUCIÓN COMPACTA ---
c1, c2 = st.columns([1, 2])

with c1:
    st.write("### ⏱️ Cronómetro")
    placeholder_tiempo = st.empty()
    col_t1, col_t2, col_t3 = st.columns(3)
    if col_t1.button("▶️"): st.session_state.corriendo = True
    if col_t2.button("⏸️"): st.session_state.corriendo = False
    if col_t3.button("🔄"): st.session_state.tiempo = 0
    
    st.markdown("### Equipos")
    c_loc, c_vis = st.columns(2)
    eq_loc = c_loc.text_input("Local:", "LOC", max_chars=3).upper()
    eq_vis = c_vis.text_input("Visita:", "VIS", max_chars=3).upper()

with c2:
    st.write("### Botonera")
    def btn_g(lab, cat, val, col):
        col.button(lab, type="primary" if st.session_state[cat]==val else "secondary", 
                   on_click=set_opcion, args=(cat, val), use_container_width=True)

    # Orden estricto y compacto
    c = st.columns(2); btn_g(eq_loc,'Eq',eq_loc,c[0]); btn_g(eq_vis,'Eq',eq_vis,c[1])
    c = st.columns(2); btn_g("Gol",'Res',"Gol",c[0]); btn_g("No gol",'Res',"No Gol",c[1])
    c = st.columns(2); btn_g("Pos",'Fase',"Pos",c[0]); btn_g("Tra",'Fase',"Tra",c[1])
    c = st.columns(3); btn_g("Par",'Err',"Par",c[0]); btn_g("Per",'Err',"Per",c[1]); btn_g("Fue",'Err',"Fue",c[2])
    c = st.columns(6); btn_g("Lar",'Tipo',"Lar",c[0]); btn_g("Pen",'Tipo',"Pen",c[1]); btn_g("Ext",'Tipo',"Ext",c[2]); btn_g("Piv",'Tipo',"Piv",c[3]); btn_g("Unf",'Tipo',"Unf",c[4]); btn_g("Dir",'Tipo',"Dir",c[5])
    c = st.columns(3); btn_g("Cent",'Lado',"Cent",c[0]); btn_g("Izq",'Lado',"Izq",c[1]); btn_g("Der",'Lado',"Der",c[2])
    
    # Portería compacta
    c = st.columns(3); z1=c[0].button("Z1"); z2=c[1].button("Z2"); z3=c[2].button("Z3")
    c = st.columns(3); z4=c[0].button("Z4"); z5=c[1].button("Z5"); z6=c[2].button("Z6")
    c = st.columns(3); z7=c[0].button("Z7"); z8=c[1].button("Z8"); z9=c[2].button("Z9")
    
    extra = st.text_input("Extra:")
    if st.button("✅ REGISTRAR JUGADA", type="primary", use_container_width=True):
        z_sel = next((f"Z{i}" for i, b in enumerate([z1,z2,z3,z4,z5,z6,z7,z8,z9], 1) if b), "N/A")
        st.session_state.eventos.append({"Time": st.session_state.tiempo, "Eq": st.session_state.Eq, "Res": st.session_state.Res, "Fase": st.session_state.Fase, "Err": st.session_state.Err if st.session_state.Err != "N/A" else "", "Tipo": st.session_state.Tipo, "Lado": st.session_state.Lado, "Zona": z_sel, "Extra": extra})
        for k in estados: st.session_state[k] = estados[k]
        st.rerun()

# Bucle del cronómetro fuera de los botones para no trabar la interfaz
if st.session_state.corriendo:
    time.sleep(1)
    st.session_state.tiempo += 1
    st.rerun()
placeholder_tiempo.metric("Segundos", st.session_state.tiempo)
