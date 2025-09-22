from __future__ import annotations
import os, io, base64, json
from datetime import datetime, timedelta
from typing import List, Dict, Any
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from app.backend.routers import health, metrics, stats, ml, etl, gold, extras
from app.services.data import load_sales_df, compute_summary
from app.core.utils import init_db_if_needed
import logging
import pandas as pd

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

app.mount("/public", StaticFiles(directory="public"), name="public")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SalesItem(BaseModel):
    date: str
    product: str
    quantity: int
    unit_price: float
    total: float

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    # Carrega os dados de vendas
    df = load_sales_df()
    
    # Converte para o formato necessário para o frontend
    sales_data = []
    if not df.empty:
        # Converte as datas para string no formato YYYY-MM-DD
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        # Converte para dicionário e depois para JSON
        sales_data = df.to_dict('records')
    
    # Obtém a lista de produtos únicos para o filtro
    products = df['product'].unique().tolist() if not df.empty else []
    
    # Calcula o resumo
    summary = compute_summary(df)
    
    # Prepara dados para o preview da API
    sales_preview = sales_data[:20]  # Apenas as primeiras 20 entradas para o preview

    power_bi_url = os.getenv("POWER_BI_EMBED_URL", "")
    
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "summary": summary,
            "sales": sales_data,
            "products": products,
            "sales_preview": sales_preview,
            "power_bi_url": power_bi_url,
            "year": datetime.utcnow().year,
        },
    )

@app.get("/api/sales")
async def get_sales(
    start_date: str = None, 
    end_date: str = None, 
    product: str = None,
    page: int = 1, 
    page_size: int = 10,
    sort_by: str = "date",
    sort_order: str = "desc"
):
    try:
        # Carrega os dados
        df = load_sales_df()
        
        # Filtra por data, se fornecido
        if start_date:
            start_date = pd.to_datetime(start_date)
            df = df[df['date'] >= start_date]
        if end_date:
            end_date = pd.to_datetime(end_date)
            # Adiciona um dia para incluir o dia final
            end_date = end_date + timedelta(days=1)
            df = df[df['date'] <= end_date]
            
        # Filtra por produto, se fornecido
        if product:
            df = df[df['product'] == product]
        
        # Ordena os dados
        df = df.sort_values(
            by=sort_by, 
            ascending=(sort_order.lower() == 'asc')
        )
        
        # Calcula a paginação
        total_items = len(df)
        total_pages = (total_items + page_size - 1) // page_size
        
        # Aplica a paginação
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_data = df.iloc[start_idx:end_idx]
        
        # Converte para o formato de dicionário
        result = {
            "data": paginated_data.to_dict('records'),
            "pagination": {
                "total_items": total_items,
                "total_pages": total_pages,
                "current_page": page,
                "page_size": page_size
            }
        }
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/summary")
async def get_summary(start_date: str = None, end_date: str = None, product: str = None):
    try:
        df = load_sales_df()
        
        # Aplica filtros
        if start_date:
            start_date = pd.to_datetime(start_date)
            df = df[df['date'] >= start_date]
        if end_date:
            end_date = pd.to_datetime(end_date)
            end_date = end_date + timedelta(days=1)  # Inclui o dia final
            df = df[df['date'] <= end_date]
        if product:
            df = df[df['product'] == product]
        
        # Calcula as métricas
        total_revenue = df['total'].sum()
        total_quantity = df['quantity'].sum()
        avg_ticket = total_revenue / len(df) if len(df) > 0 else 0
        
        # Calcula a variação em relação ao período anterior
        # (simulação - em um cenário real, você compararia com o período anterior)
        variation = {
            'revenue': 0.0,
            'quantity': 0,
            'avg_ticket': 0.0
        }
        
        # Top produtos por receita
        top_products = df.groupby('product')['total'].sum().nlargest(5).to_dict()
        
        return {
            'total_revenue': round(total_revenue, 2),
            'total_quantity': int(total_quantity),
            'avg_ticket': round(avg_ticket, 2),
            'variation': variation,
            'top_products': top_products
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/charts/revenue")
async def get_revenue_chart(period: str = 'month', product: str = None):
    try:
        df = load_sales_df()
        
        # Filtra por produto, se fornecido
        if product:
            df = df[df['product'] == product]
        
        # Agrupa por período
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        now = datetime.now()
        labels = []
        data = []
        
        if period == 'week':
            # Últimos 7 dias
            for i in range(6, -1, -1):
                date = now - timedelta(days=i)
                day_data = df[df['date'].dt.date == date.date()]
                labels.append(date.strftime('%a'))
                data.append(day_data['total'].sum())
        elif period == 'month':
            # Últimos 30 dias
            for i in range(29, -1, -1):
                date = now - timedelta(days=i)
                day_data = df[df['date'].dt.date == date.date()]
                labels.append(date.strftime('%d/%m') if i % 5 == 0 else '')
                data.append(day_data['total'].sum())
        else:  # year
            # Últimos 12 meses
            for i in range(11, -1, -1):
                date = now - pd.DateOffset(months=i)
                month_data = df[(df['date'].dt.year == date.year) & 
                               (df['date'].dt.month == date.month)]
                labels.append(date.strftime('%b %Y'))
                data.append(month_data['total'].sum())
        
        return {
            'labels': labels,
            'data': data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/charts/categories")
async def get_categories_chart(start_date: str = None, end_date: str = None):
    try:
        df = load_sales_df()
        
        # Filtra por data, se fornecido
        if start_date:
            start_date = pd.to_datetime(start_date)
            df = df[df['date'] >= start_date]
        if end_date:
            end_date = pd.to_datetime(end_date)
            end_date = end_date + timedelta(days=1)  # Inclui o dia final
            df = df[df['date'] <= end_date]
        
        # Agrupa por categoria (no exemplo, usamos 'product' como categoria)
        category_data = df.groupby('product')['total'].sum().sort_values(ascending=False).head(5)
        
        return {
            'labels': category_data.index.tolist(),
            'data': category_data.values.tolist()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Routers API
app.include_router(health.router)
app.include_router(metrics.router)
app.include_router(stats.router)
app.include_router(ml.router)
app.include_router(etl.router)
app.include_router(gold.router)
app.include_router(extras.router)
