from __future__ import annotations
import os, io, base64
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.backend.routers import health, metrics, stats, ml, etl, gold, extras
from app.services.data import load_sales_df, compute_summary
from app.core.utils import init_db_if_needed
import logging

try:
    # Inicializa o banco de dados, se necessário
    init_db_if_needed()
    logging.info("[STARTUP] Banco inicializado ou já existente.")
except Exception as e:
    logging.error(f"[STARTUP] Erro ao inicializar banco: {e}")

try:
    templates = Jinja2Templates(directory="app/templates")
    logging.info("[STARTUP] Templates Jinja2 inicializados.")
except Exception as e:
    logging.error(f"[STARTUP] Erro ao inicializar templates: {e}")

app = FastAPI(title="Moura Stack API", version="1.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):  # type: ignore[override]
    df = load_sales_df()
    summary = compute_summary(df)
    # Plotly
    plot_html = ""
    if not df.empty:
        import plotly.express as px
        grp = df.groupby("product", as_index=False)["total"].sum().sort_values("total", ascending=False)
        fig = px.bar(grp, x="product", y="total", title="Receita por Produto")
        plot_html = fig.to_html(include_plotlyjs="cdn", full_html=False)
    # Seaborn / Matplotlib estático
    scatter_b64 = ""
    if not df.empty:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import seaborn as sns
        fig2, ax = plt.subplots(figsize=(4,3))
        sns.scatterplot(data=df, x="quantity", y="unit_price", ax=ax, s=40)
        ax.set_title("Quantidade x Preço")
        ax.grid(alpha=0.2)
        buf = io.BytesIO()
        fig2.tight_layout()
        fig2.savefig(buf, format="png")
        plt.close(fig2)
        buf.seek(0)
        scatter_b64 = base64.b64encode(buf.read()).decode()
    power_bi_url = os.getenv("POWER_BI_EMBED_URL", "")
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "summary": summary,
            "plot_html": plot_html,
            "power_bi_url": power_bi_url,
            "scatter_b64": scatter_b64,
            "year": datetime.utcnow().year,
        },
    )

# Routers API
app.include_router(health.router)
app.include_router(metrics.router)
app.include_router(stats.router)
app.include_router(ml.router)
app.include_router(etl.router)
app.include_router(gold.router)
app.include_router(extras.router)
