{\rtf1\ansi\ansicpg1252\cocoartf2867
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 cat << 'EOF' > app.py\
import streamlit as st\
import pandas as pd\
import plotly.graph_objects as go\
\
st.set_page_config(page_title="Power of One: Bilansi p\'f5hine", layout="wide")\
\
st.title("\uc0\u55357 \u56960  Power of One: Finantsm\'f5ju (Bilansi p\'f5hine)")\
st.markdown("Sisesta oma kasumiaruande ja bilansi n\'e4itajad ning vaata, kuidas muudatused rahavoogu m\'f5jutavad.")\
\
# --- SIDEBAR: SISENDID ---\
st.sidebar.header("1. Kasumiaruanne")\
rev_base = st.sidebar.number_input("Aastane m\'fc\'fcgitulu (\'80)", value=10000000)\
cogs_total_base = st.sidebar.number_input("Aastane COGS (\'80)", value=6000000)\
oh_base = st.sidebar.number_input("Aastased p\'fcsikulud (\'80)", value=2500000)\
tax_rate = st.sidebar.number_input("Tulumaksum\'e4\'e4r (nt. 0.2)", value=0.2)\
\
st.sidebar.header("2. Bilansilised j\'e4\'e4gid")\
ar_base = st.sidebar.number_input("Ostjate v\'f5lgnevused (AR) (\'80)", value=1232876)\
inv_base = st.sidebar.number_input("Varud (Inventory) (\'80)", value=986301)\
ap_base = st.sidebar.number_input("Hankijate v\'f5lgnevused (AP) (\'80)", value=493150)\
\
# --- ARVUTAME P\'c4EVAD (BAASTASE) ---\
dso_base = (ar_base / rev_base) * 365 if rev_base > 0 else 0\
dio_base = (inv_base / cogs_total_base) * 365 if cogs_total_base > 0 else 0\
dpo_base = (ap_base / cogs_total_base) * 365 if cogs_total_base > 0 else 0\
\
st.sidebar.info(f"Sinu hetkeseis: DSO \{dso_base:.1f\} | DIO \{dio_base:.1f\} | DPO \{dpo_base:.1f\}")\
\
# --- PEALEHT: MUUDATUSED ---\
st.subheader("Sinu plaanitavad muudatused")\
c1, c2, c3, c4 = st.columns(4)\
with c1: p_delta = st.slider("Hinna t\'f5us (%)", 0.0, 5.0, 1.0) / 100\
with c2: v_delta = st.slider("Mahu kasv (%)", 0.0, 5.0, 1.0) / 100\
with c3: c_delta = st.slider("COGS v\'e4hendus (%)", 0.0, 5.0, 1.0) / 100\
with c4: o_delta = st.slider("P\'fcsikulu v\'e4hendus (%)", 0.0, 5.0, 1.0) / 100\
\
st.markdown("---")\
c5, c6, c7 = st.columns(3)\
with c5: dso_change = st.number_input("DSO v\'e4hendamine (p\'e4eva)", value=-1)\
with c6: dio_change = st.number_input("DIO v\'e4hendamine (p\'e4eva)", value=-1)\
with c7: dpo_change = st.number_input("DPO suurendamine (p\'e4eva)", value=1)\
\
# --- ARVUTUSLOOGIKA ---\
# EBIT-i baastase\
ebit_base = rev_base - cogs_total_base - oh_base\
net_base = ebit_base * (1 - tax_rate)\
\
# Uus tase (EBIT)\
# Eeldus: hind ja maht m\'f5jutavad m\'fc\'fcgitulu kumulatiivselt\
rev_new = rev_base * (1 + p_delta) * (1 + v_delta)\
# COGS muutub koos mahuga ja sellele lisandub efektiivsuse s\'e4\'e4st\
cogs_new = cogs_total_base * (1 + v_delta) * (1 - c_delta)\
oh_new = oh_base * (1 - o_delta)\
ebit_new = rev_new - cogs_new - oh_new\
net_new = ebit_new * (1 - tax_rate)\
\
# K\'e4ibekapitali (NWC) vabastamine\
# Baas NWC\
nwc_base = ar_base + inv_base - ap_base\
\
# Uus NWC (arvutatud uute p\'e4evade ja uute mahtude pealt)\
nwc_new_ar = (rev_new / 365) * (dso_base + dso_change)\
nwc_new_inv = (cogs_new / 365) * (dio_base + dio_change)\
nwc_new_ap = (cogs_new / 365) * (dpo_base + dpo_change)\
nwc_new = nwc_new_ar + nwc_new_inv - nwc_new_ap\
\
nwc_release = nwc_base - nwc_new \
total_cash_impact = (net_new - net_base) + nwc_release\
\
# --- VISUALISEERIMINE ---\
st.divider()\
m1, m2, m3 = st.columns(3)\
m1.metric("Kasumi kasv (p\'e4rast makse)", f"\{net_new - net_base:,.0f\} \'80")\
m2.metric("Vabanenud raha bilansist", f"\{nwc_release:,.0f\} \'80")\
m3.metric("KOGU RAHAVOO V\'d5IT", f"\{total_cash_impact:,.0f\} \'80")\
\
# Waterfall\
impacts = \{\
    "Hinna/Mahu m\'f5ju": (rev_new - rev_base - (cogs_total_base * v_delta)) * (1-tax_rate),\
    "Kulude s\'e4\'e4st": (cogs_total_base * (1+v_delta) * c_delta + (oh_base - oh_new)) * (1-tax_rate),\
    "K\'e4ibekapitali efekt": nwc_release\
\}\
\
fig = go.Figure(go.Waterfall(\
    orientation = "v",\
    measure = ["relative", "relative", "relative", "total"],\
    x = list(impacts.keys()) + ["KOGUV\'d5IT"],\
    y = list(impacts.values()) + [total_cash_impact],\
    text = [f"\{v:,.0f\} \'80" for v in impacts.values()] + [f"\{total_cash_impact:,.0f\} \'80"],\
    textposition = "outside",\
    connector = \{"line":\{"color":"rgb(63, 63, 63)"\}\},\
))\
\
fig.update_layout(title = "Kust tuleb sinu v\'f5it?", height=500)\
st.plotly_chart(fig, use_container_width=True)\
\
st.write(f"**Selgitus:** Kui suudad v\'e4hendada DSO-d \{abs(dso_change)\} p\'e4eva v\'f5rra, vabaneb bilansist t\'e4iendavalt \{(abs(dso_change) * (rev_new/365)):,.0f\} \'80.")\
EOF}
