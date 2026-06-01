import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="Dashboard Moura TI", layout="wide")
st.markdown("<h1 style='text-align:center;color:#1a56db'>Moura TI - Dashboard de Produção</h1>", unsafe_allow_html=True)


@st.cache_data
def load_data():
    data_dir = Path(__file__).parent.parent.parent.parent / "data" / "sample"
    csv_files = list(data_dir.glob("*.csv"))
    if csv_files:
        return pd.read_csv(csv_files[0], encoding="utf-8-sig")

    rng = np.random.default_rng(42)
    return pd.DataFrame({
        "data": pd.date_range("2024-01-01", periods=365, freq="D"),
        "produto": rng.choice(["Automotiva", "Estacionária", "Industrial"], 365),
        "quantidade": rng.integers(50, 500, 365),
        "receita": rng.uniform(5000, 50000, 365).round(2),
        "regiao": rng.choice(["Norte", "Nordeste", "Sudeste", "Sul", "CO"], 365),
        "eficiencia": rng.uniform(75, 100, 365).round(1),
    })


df = load_data()
df["data"] = pd.to_datetime(df["data"])

col1, col2, col3, col4 = st.columns(4)
col1.metric("Receita Total", f"R$ {df['receita'].sum():,.0f}")
col2.metric("Unidades Produzidas", f"{df['quantidade'].sum():,}")
col3.metric("Eficiência Média", f"{df['eficiencia'].mean():.1f}%")
col4.metric("Produtos", df["produto"].nunique())

st.divider()

tab1, tab2, tab3, tab4 = st.tabs(["Série Temporal", "Distribuição", "Machine Learning", "Relatório IA"])

with tab1:
    daily = df.groupby("data").agg({"receita": "sum", "quantidade": "sum"}).reset_index()
    fig = px.line(daily, x="data", y=["receita", "quantidade"],
                  title="Receita e Quantidade ao Longo do Tempo")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    col_a, col_b = st.columns(2)
    with col_a:
        fig = px.bar(df.groupby("produto")["quantidade"].sum().reset_index(),
                     x="produto", y="quantidade", title="Volume por Produto",
                     color="produto")
        st.plotly_chart(fig, use_container_width=True)
    with col_b:
        fig = px.pie(df.groupby("regiao")["receita"].sum().reset_index(),
                     values="receita", names="regiao", title="Receita por Região")
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Predição de Eficiência (Regressão)")
    features = {}
    cols = st.columns(4)
    for i, feat in enumerate(["temp_ambiente", "umidade", "velocidade_producao", "qualidade_insumo"]):
        with cols[i]:
            features[feat] = st.number_input(feat.replace("_", " ").title(), value=75.0, step=1.0)

    if st.button("Prever Eficiência"):
        try:
            from ..ml.regressor import predict_regression
            pred, importance = predict_regression(list(features.values()))
            st.success(f"Eficiência Prevista: {pred:.1f}%")
            if importance:
                fig = px.bar(x=list(importance.keys()), y=list(importance.values()),
                             title="Importância das Features")
                st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Execute o treinamento primeiro: {e}")

with tab4:
    st.subheader("Relatório Gerado por IA")
    if st.button("Gerar Relatório"):
        summary = {
            "periodo": f"{df['data'].min().date()} a {df['data'].max().date()}",
            "receita": float(df["receita"].sum()),
            "volume": int(df["quantidade"].sum()),
            "eficiencia": round(float(df["eficiencia"].mean()), 1),
            "taxa_falhas": round(float((df["eficiencia"] < 80).mean() * 100), 1),
            "custo_operacional": float(df["receita"].sum() * 0.65),
        }
        try:
            from ..llm.generators import ReportGenerator
            gen = ReportGenerator()
            report = gen.generate_technical_report(summary)
            st.markdown(report)
        except Exception as e:
            st.info(f"Relatório offline: {e}")
            st.json(summary)

st.divider()
st.caption("Moura TI - Projeto Portfólio | Analista de Desenvolvimento TI JR")
