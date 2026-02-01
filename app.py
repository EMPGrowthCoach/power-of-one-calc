import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Power of One", layout="wide")
st.title("📊 Power of One: Finantsmõju kalkulaator")

# Külgriba sisendid
st.sidebar.header("1. Kasumiaruanne")
rev_base = st.sidebar.number_input("Aastane müügitulu (€)", value=10000000)
cogs_base = st.sidebar.number_input("Aastane COGS (€)", value=6000000)
opex_base = st.sidebar.number_input("Aastased püsikulud (€)", value=250000)

# Arvutused (1% parandus)
current_profit = rev_base - cogs_base - opex_base
new_rev = rev_base * 1.01
new_cogs = cogs_base * 0.99
new_profit = new_rev - new_cogs - opex_base

# Waterfall graafik
fig = go.Figure(go.Waterfall(
    name = "Kasum", orientation = "v",
    measure = ["relative", "relative", "total"],
    x = ["Algne kasum", "1% parandus", "Uus kasum"],
    y = [current_profit, new_profit - current_profit, new_profit],
    connector = {"line":{"color":"rgb(63, 63, 63)"}},
))

st.plotly_chart(fig, use_container_width=True)
