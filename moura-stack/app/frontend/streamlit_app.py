from __future__ import annotations
import os, io
import httpx
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Moura Dash", layout="wide")

BACKEND_BASE_URL = os.getenv("BACKEND_BASE_URL", "http://localhost:8000")
POWER_BI_EMBED_URL = os.getenv("POWER_BI_EMBED_URL", "")

st.title("🔋 Moura – Dados & APIs (FastAPI + Streamlit + Power BI)")

with st.sidebar:
    st.header("Status")
    try:
        r = httpx.get(f"{BACKEND_BASE_URL}/health", timeout=5)
        status = r.json()
        st.success(f"API: {status['status']} v{status['version']} | DB: {'OK' if status['db_ok'] else 'NOK'}")
    except Exception as e:
        st.error(f"API indisponível: {e}")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📦 Amostra de Vendas (API)")
    try:
        r = httpx.get(f"{BACKEND_BASE_URL}/metrics/sales?limit=500", timeout=10)
        data = r.json()
        df = pd.DataFrame(data["preview"])
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao carregar vendas: {e}")
        df = pd.DataFrame()

with col2:
    st.subheader("📊 Resumo (API)")
    try:
        s = httpx.get(f"{BACKEND_BASE_URL}/metrics/summary", timeout=10).json()
        c1, c2, c3 = st.columns(3)
        c1.metric("Receita Total", f"R$ {s['total_revenue']:.2f}")
        c2.metric("Qtd Total", s["total_quantity"])
        c3.metric("Ticket Médio", f"R$ {s['avg_ticket']:.2f}")
        st.caption(f"Top produtos: {', '.join(s['top_products'])}")
        st.caption(f"Regiões: {', '.join(s['regions'])}")
    except Exception as e:
        st.error(f"Erro ao carregar resumo: {e}")

if not df.empty:
    st.subheader("📈 Receita por Produto (Plotly)")
    fig = px.bar(df.groupby("product", as_index=False)["total"].sum(), x="product", y="total")
    st.plotly_chart(fig, use_container_width=True)

if not df.empty:
    st.subheader("🖼️ Dispersão quantidade vs. preço (Seaborn/Matplotlib)")
    fig2, ax = plt.subplots()
    sns.scatterplot(data=df, x="quantity", y="unit_price", ax=ax)
    ax.set_title("Quantidade x Preço Unitário")
    st.pyplot(fig2)

st.subheader("🧪 Estatística/ML")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("Pearson (quantity ~ unit_price)"):
        try:
            res = httpx.get(f"{BACKEND_BASE_URL}/stats/pearson", timeout=10).json()
            st.success(f"r = {res['pearson_r']:.4f} | p = {res['p_value']:.4f}")
        except Exception as e:
            st.error(f"Erro: {e}")
with c2:
    if st.button("OLS: total ~ quantity + unit_price"):
        try:
            ols = httpx.get(f"{BACKEND_BASE_URL}/stats/ols", timeout=10).json()
            st.write("Parâmetros:", ols["params"])
            st.write("R²:", round(ols["r2"], 4))
        except Exception as e:
            st.error(f"Erro: {e}")
with c3:
    train = st.button("Treinar Regressão Linear (sklearn)")
    if train:
        try:
            resp = httpx.post(f"{BACKEND_BASE_URL}/ml/train", timeout=15).json()
            st.success(f"R²={resp['r2']:.4f}; coef={resp['coef']}; b0={resp['intercept']:.2f}")
        except Exception as e:
            st.error(f"Erro: {e}")
qty = st.number_input("quantity", min_value=0, value=10)
price = st.number_input("unit_price", min_value=0.0, value=200.0, step=10.0)
if st.button("Prever total"):
    try:
        pred = httpx.post(f"{BACKEND_BASE_URL}/ml/predict", json={"quantity": qty, "unit_price": price}, timeout=10).json()
        st.info(f"y_pred ≈ R$ {pred['y_pred']:.2f}")
    except Exception as e:
        st.error(f"Erro: {e}")

st.subheader("🛠️ Operações")
oc1, oc2, oc3 = st.columns(3)
with oc1:
    if st.button("Disparar ETL (Prefect)"):
        try:
            res = httpx.post(f"{BACKEND_BASE_URL}/etl/run", timeout=30).json()
            st.success(res)
        except Exception as e:
            st.error(f"Erro: {e}")
with oc2:
    if st.button("Exportar GOLD (Parquet/CSV)"):
        try:
            res = httpx.post(f"{BACKEND_BASE_URL}/gold/export", timeout=30).json()
            st.success(res)
        except Exception as e:
            st.error(f"Erro: {e}")

st.subheader("📑 Power BI")
if POWER_BI_EMBED_URL:
    st.components.v1.iframe(src=POWER_BI_EMBED_URL, height=600, scrolling=True)
else:
    st.info("Defina POWER_BI_EMBED_URL no .env para exibir seu relatório do Power BI.")
