import streamlit as st
import pandas as pd
import time

st.set_page_config(layout="wide", page_title="Handball Tagger Live")

# --- ESTADO Y LÓGICA DEL CRONÓMETRO ---
if 'eventos' not in st.session_state: st.session_state.eventos = []
if 'tiempo' not in st.session_state: st.session_state.tiempo = 0
if 'corriendo' not in st.session_state: st.session_state.corriendo = False

# Estados de botones
estados = {'Eq': 'LOC', 'Res': 'Gol', 'Fase': 'Pos', 'Err': 'N/A', 'Tipo': 'Lar', 'Lado': 'Cent', 'Zona': 'N/A'}
for k, v in estados.items():
    if k not in st.session_state: st.session_state[k] = v

def set_opcion(cat, val): st.session_state[cat] = val

# --- INTERFAZ ---
st.title("Panel de Análisis Táctico - En Vivo")

c_cron, c_eq = st.columns([1, 1])

with c_cron:
    st.write("### ⏱️ Cronómetro")
    col_t1, col_t2, col_t3 = st.columns(3)
    if col_t1.button("▶️ Iniciar"): st.session_state.corriendo = True
    if col_t2.button("⏸️ Pausar"): st.session_state.corriendo = False
    if col_t3.button("🔄 Reset"): 
        st.session_state.corriendo = False
        st.session_state.tiempo = 0
    
    if st.session_state.corriendo:
        time.sleep(1)
        st.session_state.tiempo += 1
        st.rerun()
    
    st.metric("Tiempo actual (segundos)", st.session_state.tiempo)

with c_eq:
    st.markdown("### Configuración de Equipos")
    c_loc, c_vis = st.columns(2)
    eq_loc = c_loc.text_input("Local:", "LOC", max_chars=3).upper()
    eq_vis = c_vis.text_input("Visita:", "VIS", max_chars=3).upper()

# --- BOTONERA ---
def btn_g(lab, cat, val, col):
    col.button(lab, type="primary" if st.session_state[cat]==val else "secondary", 
               on_click=set_opcion, args=(cat, val), use_container_width=True)

st.write("---")
st.write("**Equipo**"); c=st.columns(2); btn_g(eq_loc,'Eq',eq_loc,c[0]); btn_g(eq_vis,'Eq',eq_vis,c[1])
st.write("**Resultado**"); c=st.columns(2); btn_g("Gol",'Res',"Gol",c[0]); btn_g("No gol",'Res',"No Gol",c[1])
st.write("**Fase**"); c=st.columns(2); btn_g("Pos",'Fase',"Pos",c[0]); btn_g("Tra",'Fase',"Tra",c[1])
st.write("**Error**"); c=st.columns(3); btn_g("Par",'Err',"Par",c[0]); btn_g("Per",'Err',"Per",c[1]); btn_g("Fue",'Err',"Fue",c[2])
st.write("**Tipo**"); c1=st.columns(3); btn_g("Lar",'Tipo',"Lar",c1[0]); btn_g("Pen",'Tipo',"Pen",c1[1]); btn_g("Ext",'Tipo',"Ext",c1[2])
c2=st.columns(3); btn_g("Piv",'Tipo',"Piv",c2[0]); btn_g("Unf",'Tipo',"Unf",c2[1]); btn_g("Dir",'Tipo',"Dir",c2[2])
st.write("**Lado**"); c=st.columns(3); btn_g("Cent",'Lado',"Cent",c[0]); btn_g("Izq",'Lado',"Izq",c[1]); btn_g("Der",'Lado',"Der",c[2])

st.write("🥅 **Matriz de Portería**")
z = st.columns(3); z1=z[0].button("Z1"); z2=z[1].button("Z2"); z3=z[2].button("Z3")
z = st.columns(3); z4=z[0].button("Z4"); z5=z[1].button("Z5"); z6=z[2].button("Z6")
z = st.columns(3); z7=z[0].button("Z7"); z8=z[1].button("Z8"); z9=z[2].button("Z9")

extra = st.text_input("Extra:")
btn_st = st.button("✅ REGISTRAR JUGADA", type="primary", use_container_width=True)

if any([z1,z2,z3,z4,z5,z6,z7,z8,z9]):
    set_opcion('Zona', next(f"Z{i}" for i, b in enumerate([z1,z2,z3,z4,z5,z6,z7,z8,z9], 1) if b))

if btn_st:
    st.session_state.eventos.append({
        "Time": st.session_state.tiempo,
        "Eq": st.session_state.Eq, "Res": st.session_state.Res, "Fase": st.session_state.Fase,
        "Err": st.session_state.Err if st.session_state.Err != "N/A" else "",
        "Tipo": st.session_state.Tipo, "Lado": st.session_state.Lado,
        "Zona": st.session_state.Zona, "Extra": extra
    })
    for k in estados: st.session_state[k] = estados[k]
    st.rerun()

if len(st.session_state.eventos) > 0:
    st.dataframe(pd.DataFrame(st.session_state.eventos), use_container_width=True)
    st.download_button("📥 Descargar CSV", data=pd.DataFrame(st.session_state.eventos).to_csv(index=False).encode('utf-8'), file_name='partido_vivo.csv', mime='text/csv')
