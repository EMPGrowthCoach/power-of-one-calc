import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Power of One: Strategiline", layout="wide")

st.title("🚀 Power of One: Finantsmõju & Raha Tsükkel")

# --- SIDEBAR: SISENDID ---
st.sidebar.header("1. Kasumiaruanne")
rev_base = st.sidebar.number_input("Aastane müügitulu (€)", value=10000000)
cogs_base = st.sidebar.number_input("Aastane COGS (€)", value=6000000)
opex_base = st.sidebar.number_input("Aastased püsikulud (€)", value=2500000)
tax_rate = st.sidebar.number_input("Tulumaksumäär (nt. 0.2)", value=0.20)

st.sidebar.header("2. Bilansilised jäägid")
ar_base = st.sidebar.number_input("Ostjate võlgnevused (AR) (€)", value=1232876)
inv_base = st.sidebar.number_input("Varud (Inventory) (€)", value=986301)
ap_base = st.sidebar.number_input("Hankijate võlgnevused (AP) (€)", value=493150)

# --- ARVUTUSLOOGIKA (HETKESEIS) ---
dso = (ar_base / rev_base) * 365
dio = (inv_base / cogs_base) * 365
dpo = (ap_base / cogs_base) * 365
ccc = dso + dio - dpo

wc_invested = ar_base + inv_base - ap_base
ebitda_base = rev_base - cogs_base - opex_base
# Ühe pöörde tootlikkus: Mitu eurot EBITDA-d toodab 1€ WC-d
productivity = ebitda_base / wc_invested if wc_invested > 0 else 0

# --- PEALEHT: STRATEEGILISED NÄITAJAD ---
st.subheader("Sinu ettevõtte raha liikumise kiirus")
c1, c2, c3 = st.columns(3)

with c1:
    st.info(f"**Cash Conversion Cycle (CCC)**\n\n# {ccc:.1f} päeva")
    st.caption("Aeg, mil raha on kinni protsessides (DSO+DIO-DPO).")

with c2:
    st.success(f"**WC investeeringu tootlikkus**\n\n# {productivity:.2f} €")
    st.caption("Iga käibekapitali investeeritud 1 € toodab nii palju EBITDA-d.")

with c3:
    st.metric("Investeeritud käibekapital", f"{wc_invested:,.0f} €")
    st.caption("Summa, mis on hetkel bilansis kinni.")

st.divider()

# --- MUUDATUSED JA MÕJU ---
st.subheader("Simuleeri 1% ja protsesside parandamist")
col1, col2, col3, col4 = st.columns(4)
p_inc = col1.slider("Hinna tõus (%)", 0.0, 5.0, 1.0)
v_inc = col2.slider("Mahu kasv (%)", 0.0, 5.0, 1.0)
dso_adj = col3.slider("DSO parandus (päeva)", -10, 10, -1)
dio_adj = col4.slider("DIO parandus (päeva)", -10, 10, -1)

# Uue seisu arvutus
new_rev = rev_base * (1 + p_inc/100) * (1 + v_inc/100)
new_cogs = cogs_base * (1 + v_inc/100)
new_ebitda = new_rev - new_cogs - opex_base
profit_impact = (new_ebitda - ebitda_base) * (1 - tax_rate)

# Rahavoo vabanemine päevade parandusest
cash_freed = ((abs(dso_adj) * new_rev) / 365) + ((abs(dio_adj) * new_cogs) / 365)
total_impact = profit_impact + cash_freed

# --- VISUALISEERIMINE ---
m1, m2 = st.columns(2)
m1.metric("KOGU RAHALINE VÕIT", f"{total_impact:,.0f} €", f"{total_impact/rev_base*100:.2f}% käibest")

fig = go.Figure(go.Waterfall(
    orientation = "v",
    measure = ["relative", "relative", "total"],
    x = ["Kasumi kasv (neto)", "Vabanenud raha (CCC)", "KOKKU"],
    y = [profit_impact, cash_freed, total_impact],
    connector = {"line":{"color":"rgb(63, 63, 63)"}},
))
st.plotly_chart(fig, use_container_width=True)
