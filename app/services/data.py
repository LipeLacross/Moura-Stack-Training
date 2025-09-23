from __future__ import annotations
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple, Union
import pandas as pd
import numpy as np
from sqlalchemy import text
from app.backend.db import engine
from sklearn.linear_model import LinearRegression
from scipy.stats import pearsonr
import statsmodels.api as sm
import logging

_MODEL: LinearRegression | None = None

# Cache para armazenar dados em memória
_CACHED_DATA: Optional[pd.DataFrame] = None
_LAST_UPDATE: Optional[datetime] = None
CACHE_TTL_MINUTES = 5  # Tempo em minutos para o cache expirar

# TODO(refactor, 2025-09-18, consolidar validações de schema se dado crescer)

def load_sales_df(use_cache: bool = True, start_date: str = None, end_date: str = None, product: str = None) -> pd.DataFrame:
    """
    Carrega os dados de vendas do banco de dados ou CSV, aplicando filtros opcionais.

    Args:
        use_cache: Se True, usa os dados em cache se disponíveis e não expirados
        start_date: Data inicial (YYYY-MM-DD)
        end_date: Data final (YYYY-MM-DD)
        product: Nome do produto para filtrar

    Returns:
        DataFrame com os dados de vendas filtrados
    """
    global _CACHED_DATA, _LAST_UPDATE
    
    # Sanitiza o parâmetro 'product' logo no início
    if product:
        product_sanitized = str(product).strip().lower()
        if product_sanitized in ['todos os produtos', 'todos', 'all', 'all products', '']:
            product = None
    logging.info(f"[DEBUG] Valor final do filtro de produto: {product}")  # TODO(copilot, 2025-09-22, debug filtro): Remover após validação

    # Verifica se pode usar o cache
    # Só usa cache se NÃO houver filtros
    if use_cache and _CACHED_DATA is not None and _LAST_UPDATE is not None:
        cache_age = datetime.now() - _LAST_UPDATE
        if cache_age < timedelta(minutes=CACHE_TTL_MINUTES):
            logging.info(f"[DEBUG] Usando cache: True")
            return _CACHED_DATA.copy()
    logging.info(f"[DEBUG] Usando cache: False")
    # ...existing code...

def compute_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calcula métricas de resumo para os dados de vendas.
    Args:
        df: DataFrame com os dados de vendas
    Returns:
        Dicionário com as métricas calculadas
    """
    # Colunas críticas
    required_cols = ['quantity', 'unit_price']
    missing_cols = [col for col in required_cols if col not in df.columns]
    # Tenta criar 'total' se possível
    if 'total' not in df.columns and not missing_cols:
        df['total'] = df['quantity'] * df['unit_price']
    # Se faltar qualquer coluna crítica, retorna métricas zeradas
    if 'total' not in df.columns or missing_cols:
        logging.warning(f"[compute_summary] Missing columns: {['total'] if 'total' not in df.columns else []} + {missing_cols} — returning zeroed metrics.")
        return {
            "total_revenue": 0.0,
            "total_quantity": 0,
            "avg_ticket": 0.0,
            "top_products": [],
            "regions": [],
            "sales_count": 0,
            "avg_quantity": 0.0,
            "unique_products": 0,
            "start_date": None,
            "end_date": None,
        }
    if df.empty:
        return {
            "total_revenue": 0.0,
            "total_quantity": 0,
            "avg_ticket": 0.0,
            "top_products": [],
            "regions": [],
            "sales_count": 0,
            "avg_quantity": 0.0,
            "unique_products": 0,
            "start_date": None,
            "end_date": None,
        }
    # Métricas básicas
    total_revenue = float(df["total"].sum()) if "total" in df.columns else 0.0
    total_quantity = int(df["quantity"].sum()) if "quantity" in df.columns else 0
    sales_count = len(df)
    avg_ticket = float(df["total"].mean()) if "total" in df.columns else 0.0
    avg_quantity = float(df["quantity"].mean()) if "quantity" in df.columns else 0.0
    # Top produtos por receita
    if "product" in df.columns and "total" in df.columns:
        product_sales = df.groupby("product")["total"].sum()
        top_products = product_sales.nlargest(5).index.tolist()
        unique_products = len(product_sales)
    else:
        top_products = []
        unique_products = 0
    # Regiões (se disponível)
    regions = sorted(df["region"].dropna().unique().tolist()) if "region" in df.columns else []
    # Período coberto
    if "date" in df.columns:
        try:
            dates = pd.to_datetime(df["date"], errors="coerce")
            start_date = dates.min()
            end_date = dates.max()
            start_date = start_date.strftime("%Y-%m-%d") if pd.notnull(start_date) else None
            end_date = end_date.strftime("%Y-%m-%d") if pd.notnull(end_date) else None
        except Exception:
            start_date = None
            end_date = None
    else:
        start_date = None
        end_date = None
    return {
        "total_revenue": total_revenue,
        "total_quantity": total_quantity,
        "avg_ticket": avg_ticket,
        "top_products": top_products,
        "regions": regions,
        "sales_count": sales_count,
        "avg_quantity": avg_quantity,
        "unique_products": unique_products,
        "start_date": start_date,
        "end_date": end_date,
    }
