import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Power of One: Finantsmõju", layout="wide")
st.title("📊 Power of One: Finantsmõju kalkulaator")

# --- KÜLGRIIBA: SISENDID ---
st.sidebar.header("1. Praegune seis")
rev = st.sidebar.number_input("Aastane müügitulu (€)", value=10000000)
cogs = st.sidebar.number_input("Aastane COGS (€)", value=6000000)
opex = st.sidebar.number_input("Aastased püsikulud (€)", value=2500000)

st.sidebar.header("2. Muudatused (1%)")
p_inc = st.sidebar.slider("Hinna muutus (%)", -5.0, 5.0, 1.0)
v_inc = st.sidebar.slider("Mahu muutus (%)", -5.0, 5.0, 1.0)
c_dec = st.sidebar.slider("COGS vähendamine (%)", -5.0, 5.0, 1.0)
o_dec = st.sidebar.slider("Püsikulude vähendamine (%)", -5.0, 5.0, 1.0)

# --- ARVUTUSED ---
current_gp = rev - cogs
current_ebitda = current_gp - opex

# Uue seisu arvutus
new_rev = rev * (1 + p_inc/100) * (1 + v_inc/100)
new_cogs = cogs * (1 - c_dec/100) * (1 + v_inc/100) # COGS sõltub mahust
new_opex = opex * (1 - o_dec/100)

new_gp = new_rev - new_cogs
new_ebitda = new_gp - new_opex
diff = new_ebitda - current_ebitda

# --- VISUALISEERIMINE ---
col1, col2 = st.columns([1, 1])

with col1:
    st.metric("Uus EBITDA", f"{new_ebitda:,.0f} €", f"{diff:,.0f} € parandus")
    
with col2:
    fig = go.Figure(go.Waterfall(
        name = "Mõju", orientation = "v",
        measure = ["relative", "relative", "total"],
        x = ["Algne EBITDA", "1% Parandused", "Uus EBITDA"],
        y = [current_ebitda, diff, new_ebitda],
        connector = {"line":{"color":"rgb(63, 63, 63)"}},
    ))
    st.plotly_chart(fig, use_container_width=True)

st.info("Nipp: Liiguta külgribal slaidereid, et näha, kuidas iga 'kang' kasumit mõjutab.")
