import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Power of One: Bilansipõhine", layout="wide")

# Pealkiri
st.title("🚀 Power of One: Finantsmõju (Bilansi põhine)")
st.markdown("Sisesta oma kasumiaruande ja bilansi näitajad ning vaata, kuidas muudatused rahavoogu mõjutavad.")

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

# --- ARVUTUSED (HETKESEIS) ---
dso_base = (ar_base / rev_base) * 365
dio_base = (inv_base / cogs_base) * 365
dpo_base = (ap_base / cogs_base) * 365
# Cash Conversion Cycle (CCC)
ccc_base = dso_base + dio_base - dpo_base
# Tootlikkus: EBITDA / (AR + Inv - AP)
current_ebitda = rev_base - cogs_base - opex_base
current_wc = ar_base + inv_base - ap_base
productivity = current_ebitda / current_wc if current_wc > 0 else 0

# --- LISA KÜLGRIBALE INFOKAST ---
st.sidebar.info(f"""
**Sinu hetkeseis:**
* DSO: {dso_base:.1f} | DIO: {dio_base:.1f} | DPO: {dpo_base:.1f}
* **CCC: {ccc_base:.1f} päeva**
* **Tootlikkus: {productivity:.2f} €** (EBITDA / WC)
""")

# --- PEALEHT: MUUDATUSED (SLAIDERID) ---
st.subheader("Sinu plaanitavad muudatused")
c1, c2, c3, c4 = st.columns(4)
p_inc = c1.slider("Hinna tõus (%)", 0.0, 5.0, 1.0)
v_inc = c2.slider("Mahu kasv (%)", 0.0, 5.0, 1.0)
c_dec = c3.slider("COGS vähendus (%)", 0.0, 5.0, 1.0)
o_dec = c4.slider("Püsikulu vähendus (%)", 0.0, 5.0, 1.0)

cc1, cc2, cc3 = st.columns(3)
dso_adj = cc1.number_input("DSO vähendamine (päeva)", value=-1)
dio_adj = cc2.number_input("DIO vähendamine (päeva)", value=-1)
dpo_adj = cc3.number_input("DPO suurendamine (päeva)", value=1)

# --- MÕJU ARVUTAMINE ---
new_rev = rev_base * (1 + p_inc/100) * (1 + v_inc/100)
new_cogs = cogs_base * (1 - c_dec/100) * (1 + v_inc/100)
new_opex = opex_base * (1 - o_dec/100)

new_ebitda = new_rev - new_cogs - new_opex
profit_gain = (new_ebitda - current_ebitda) * (1 - tax_rate)

new_dso = dso_base + dso_adj
new_dio = dio_base + dio_adj
new_dpo = dpo_base + dpo_adj

cash_from_ar = ar_base - ((new_dso * new_rev) / 365)
cash_from_inv = inv_base - ((new_dio * new_cogs) / 365)
cash_from_ap = ((new_dpo * new_cogs) / 365) - ap_base
total_wc_gain = cash_from_ar + cash_from_inv +
