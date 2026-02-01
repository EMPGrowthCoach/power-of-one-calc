import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Power of One: Bilansipõhine", layout="wide")

st.title("🚀 Power of One: Finantsmõju (Bilansi põhine)")
st.markdown("Sisesta oma andmed ning vaata, kuidas muudatused rahavoogu mõjutavad.")

# --- SIDEBAR: SISENDID (ALGANDMED) ---
st.sidebar.header("1. Kasumiaruanne")
rev_base = st.sidebar.number_input("Aastane müügitulu (€)", value=10000000)
cogs_base = st.sidebar.number_input("Aastane COGS (€)", value=6000000)
opex_base = st.sidebar.number_input("Aastased püsikulud (€)", value=2500000)
tax_rate = st.sidebar.number_input("Tulumaksumäär (nt. 0.2)", value=0.20)

st.sidebar.header("2. Bilansilised jäägid")
ar_base = st.sidebar.number_input("Ostjate võlgnevused (AR) (€)", value=1232876)
inv_base = st.sidebar.number_input("Varud (Inventory) (€)", value=986301)
ap_base = st.sidebar.number_input("Hankijate võlgnevused (AP) (€)", value=493150)

# --- PEALEHT: MUUDATUSED (SLAIDERID 0.5 SAMMUGA) ---
st.subheader("Sinu plaanitavad muudatused")
c1, c2, c3, c4 = st.columns(4)
# Lisatud step=0.5
p_inc = c1.slider("Hinna tõus (%)", 0.0, 10.0, 1.0, step=0.5)
v_inc = c2.slider("Mahu kasv (%)", 0.0, 10.0, 1.0, step=0.5)
c_dec = c3.slider("COGS vähendus (%)", 0.0, 10.0, 1.0, step=0.5)
o_dec = c4.slider("Püsikulu vähendus (%)", 0.0, 10.0, 1.0, step=0.5)

cc1, cc2, cc3 = st.columns(3)
dso_adj = cc1.number_input("DSO muutus (päeva)", value=-1)
dio_adj = cc2.number_input("DIO muutus (päeva)", value=-1)
dpo_adj = cc3.number_input("DPO muutus (päeva)", value=1)

# --- DÜNAAMILISED ARVUTUSED ---
# Uued väärtused põhinevad valitud muudatustel
current_ebitda = rev_base - cogs_base - opex_base

new_rev = rev_base * (1 + p_inc/100) * (1 + v_inc/100)
new_cogs = cogs_base * (1 - c_dec/100) * (1 + v_inc/100)
new_opex = opex_base * (1 - o_dec/100)
new_ebitda = new_rev - new_cogs - new_opex

# Päevade arvutused (Hetkeseis + Sinu sisestatud muudatused)
dso_new = ((ar_base / rev_base) * 365) + dso_adj
dio_new = ((inv_base / cogs_base) * 365) + dio_adj
dpo_new = ((ap_base / cogs_base) * 365) + dpo_adj

# DÜNAAMILINE CCC ja TOOTLIKKUS
ccc_new = dso_new + dio_new - dpo_new
wc_new = ((dso_new * new_rev) / 365) + ((dio_new * new_cogs) / 365) - ((dpo_new * new_cogs) / 365)
productivity_new = new_ebitda / wc_new if wc_new > 0 else 0

# --- DÜNAAMILINE INFOKAST KÜLGRIBAL ---
st.sidebar.info(f"""
**Sinu hetkeseis (sh muudatused):**
* DSO: {dso_new:.1f} | DIO: {dio_new:.1f} | DPO: {dpo_new:.1f}
* **CCC: {ccc_new:.1f} päeva**
* **Tootlikkus: {productivity_new:.2f} €** (EBITDA / WC)
""")

# --- MÕJU EKRAANIL ---
profit_gain = (new_ebitda - current_ebitda) * (1 - tax_rate)
cash_from_ar = ar_base - ((dso_new * new_rev) / 365)
cash_from_inv = inv_base - ((dio_new * new_cogs) / 365)
cash_from_ap = ((dpo_new * new_cogs) / 365) - ap_base
total_wc_gain = cash_from_ar + cash_from_inv + cash_from_ap
total_cash_impact = profit_gain + total_wc_gain

st.divider()
m1, m2, m3 = st.columns(3)
m1.metric("Kasumi kasv (neto)", f"{profit_gain:,.0f} €")
m2.metric("Vabanenud raha bilansist", f"{total_wc_gain:,.0f} €")
m3.metric("KOGU RAHAVOO VÕIT", f"{total_cash_impact:,.0f} €")

# Waterfall graafik
fig = go.Figure(go.Waterfall(
    orientation = "v",
    measure = ["relative", "relative", "relative", "total"],
    x = ["Kasumi mõju", "Kulude sääst", "Käibekapitali efekt", "KOGUVÕIT"],
    y = [(new_rev - rev_base) * (1-tax_rate), 
         ((cogs_base - new_cogs) + (opex_base - new_opex)) * (1-tax_rate), 
         total_wc_gain, 
         total_cash_impact],
    connector = {"line":{"color":"rgb(63, 63, 63)"}},
))
st.plotly_chart(fig, use_container_width=True)
