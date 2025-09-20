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
    
    # Verifica se pode usar o cache
    if use_cache and _CACHED_DATA is not None and _LAST_UPDATE is not None:
        cache_age = datetime.now() - _LAST_UPDATE
        if cache_age < timedelta(minutes=CACHE_TTL_MINUTES):
            return _CACHED_DATA.copy()
    
    # Carrega os dados da fonte
    source = os.getenv("ETL_SOURCE", "csv")
    if source == "postgres":
        query = """
            SELECT order_id, region, product, quantity, unit_price, COALESCE(total, quantity*unit_price) AS total, date
            FROM sales
            WHERE 1=1
        """
        params = {}
        if start_date:
            query += " AND date >= :start_date"
            params['start_date'] = start_date
        if end_date:
            query += " AND date <= :end_date"
            params['end_date'] = end_date
        if product and product.lower() != 'todos os produtos':
            query += " AND product = :product"
            params['product'] = product
        query += " ORDER BY order_id"
        with engine.connect() as conn:
            df = pd.read_sql(text(query), conn, params=params)
    else:
        csv_path = os.getenv("ETL_CSV_PATH", "data/sample_sales.csv")
        df = pd.read_csv(csv_path)
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        # Garante que a coluna 'total' existe
        if 'total' not in df.columns and 'quantity' in df.columns and 'unit_price' in df.columns:
            df['total'] = df['quantity'] * df['unit_price']
        if start_date:
            df = df[df['date'] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df['date'] <= pd.to_datetime(end_date)]
        if product and product.lower() != 'todos os produtos':
            df = df[df['product'] == product]

    # Garante que a coluna de data está no formato correto
    if 'date' not in df.columns:
        # Se não houver coluna de data, cria uma com a data atual
        df['date'] = pd.to_datetime('today')
    
    # Atualiza o cache
    _CACHED_DATA = df.copy()
    _LAST_UPDATE = datetime.now()
    
    return df

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

def get_sales_data(
    start_date: Optional[Union[str, datetime]] = None,
    end_date: Optional[Union[str, datetime]] = None,
    product: Optional[str] = None,
    region: Optional[str] = None,
    min_quantity: Optional[float] = None,
    max_quantity: Optional[float] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by: str = "date",
    sort_order: str = "desc",
    limit: Optional[int] = None,
    offset: int = 0
) -> Tuple[pd.DataFrame, int]:
    """
    Obtém dados de vendas com filtros e ordenação.
    
    Args:
        start_date: Data inicial (inclusiva)
        end_date: Data final (inclusiva)
        product: Nome do produto para filtrar
        region: Região para filtrar
        min_quantity: Quantidade mínima
        max_quantity: Quantidade máxima
        min_price: Preço unitário mínimo
        max_price: Preço unitário máximo
        sort_by: Campo para ordenação
        sort_order: Direção da ordenação ('asc' ou 'desc')
        limit: Número máximo de registros a retornar
        offset: Número de registros para pular
        
    Returns:
        Tupla com (DataFrame com os dados filtrados, total de registros)
    """
    # Carrega os dados
    df = load_sales_df()
    
    # Aplica filtros
    if start_date is not None:
        if isinstance(start_date, str):
            start_date = pd.to_datetime(start_date)
        df = df[df["date"] >= start_date]
    
    if end_date is not None:
        if isinstance(end_date, str):
            end_date = pd.to_datetime(end_date)
        # Inclui todo o dia final
        end_date = end_date + timedelta(days=1)
        df = df[df["date"] <= end_date]
    
    if product is not None:
        df = df[df["product"] == product]
    
    if region is not None and "region" in df.columns:
        df = df[df["region"] == region]
    
    if min_quantity is not None:
        df = df[df["quantity"] >= min_quantity]
    
    if max_quantity is not None:
        df = df[df["quantity"] <= max_quantity]
    
    if min_price is not None:
        df = df[df["unit_price"] >= min_price]
    
    if max_price is not None:
        df = df[df["unit_price"] <= max_price]
    
    # Ordena os resultados
    if sort_by in df.columns:
        df = df.sort_values(
            by=sort_by, 
            ascending=(sort_order.lower() == "asc")
        )
    
    # Conta o total de registros (antes da paginação)
    total = len(df)
    
    # Aplica a paginação
    if limit is not None:
        df = df[offset:offset+limit]
    
    return df, total

def get_sales_by_period(
    period: str = 'day',
    start_date: Optional[Union[str, datetime]] = None,
    end_date: Optional[Union[str, datetime]] = None,
    product: Optional[str] = None
) -> pd.DataFrame:
    """
    Agrupa vendas por período de tempo.
    
    Args:
        period: Período de agrupamento ('day', 'week', 'month', 'year')
        start_date: Data inicial (inclusiva)
        end_date: Data final (inclusiva)
        product: Nome do produto para filtrar
        
    Returns:
        DataFrame com as vendas agrupadas por período
    """
    # Carrega os dados
    df = load_sales_df()
    
    # Aplica filtros
    if start_date is not None:
        if isinstance(start_date, str):
            start_date = pd.to_datetime(start_date)
        df = df[df["date"] >= start_date]
    
    if end_date is not None:
        if isinstance(end_date, str):
            end_date = pd.to_datetime(end_date)
        # Inclui todo o dia final
        end_date = end_date + timedelta(days=1)
        df = df[df["date"] <= end_date]
    
    if product is not None:
        df = df[df["product"] == product]
    
    if df.empty:
        return pd.DataFrame(columns=['period', 'total_sales', 'total_revenue', 'avg_ticket'])
    
    # Agrupa por período
    df = df.copy()
    df['period'] = df['date'].dt.to_period(period[0].upper())
    
    # Agrega os dados
    result = df.groupby('period').agg(
        total_sales=('quantity', 'sum'),
        total_revenue=('total', 'sum'),
        avg_ticket=('total', 'mean'),
        order_count=('order_id', 'count')
    ).reset_index()
    
    # Converte o período para string
    result['period'] = result['period'].astype(str)
    
    return result

def get_top_products(
    n: int = 5,
    by: str = 'revenue',  # 'revenue' ou 'quantity'
    start_date: Optional[Union[str, datetime]] = None,
    end_date: Optional[Union[str, datetime]] = None,
    min_quantity: Optional[float] = None
) -> pd.DataFrame:
    """
    Obtém os produtos mais vendidos por receita ou quantidade.
    
    Args:
        n: Número de produtos a retornar
        by: Métrica para ordenação ('revenue' ou 'quantity')
        start_date: Data inicial (inclusiva)
        end_date: Data final (inclusiva)
        min_quantity: Quantidade mínima para filtrar
        
    Returns:
        DataFrame com os produtos mais vendidos
    """
    # Carrega os dados
    df = load_sales_df()
    
    # Aplica filtros
    if start_date is not None:
        if isinstance(start_date, str):
            start_date = pd.to_datetime(start_date)
        df = df[df["date"] >= start_date]
    
    if end_date is not None:
        if isinstance(end_date, str):
            end_date = pd.to_datetime(end_date)
        # Inclui todo o dia final
        end_date = end_date + timedelta(days=1)
        df = df[df["date"] <= end_date]
    
    if min_quantity is not None:
        df = df[df["quantity"] >= min_quantity]
    
    if df.empty:
        return pd.DataFrame(columns=['product', 'revenue', 'quantity', 'order_count'])
    
    # Agrupa por produto
    result = df.groupby('product').agg(
        revenue=('total', 'sum'),
        quantity=('quantity', 'sum'),
        order_count=('order_id', 'count'),
        avg_price=('unit_price', 'mean')
    ).reset_index()
    
    # Ordena pelo critério especificado
    sort_by = 'revenue' if by == 'revenue' else 'quantity'
    result = result.sort_values(sort_by, ascending=False).head(n)
    
    return result

def compute_pearson(df: pd.DataFrame) -> Dict[str, float]:
    """
    Calcula a correlação de Pearson entre quantidade e preço unitário.
    
    Args:
        df: DataFrame com as colunas 'quantity' e 'unit_price'
        
    Returns:
        Dicionário com o coeficiente de Pearson e o valor-p
    """
    if len(df) < 2:
        return {"pearson_r": 0.0, "p_value": 1.0}
    
    try:
        r, p = pearsonr(df["quantity"], df["unit_price"])
        return {"pearson_r": float(r), "p_value": float(p)}
    except Exception as e:
        logging.error(f"Erro ao calcular correlação de Pearson: {e}")
        return {"pearson_r": 0.0, "p_value": 1.0}

def compute_ols(df: pd.DataFrame) -> Dict[str, Any]:
    y = df["total"]
    X = df[["quantity", "unit_price"]]
    X = sm.add_constant(X, prepend=True)
    model = sm.OLS(y, X).fit()
    params = {k: float(v) for k, v in model.params.to_dict().items()}
    return {"params": params, "r2": float(model.rsquared)}

def train_model(df: pd.DataFrame) -> Dict[str, Any]:
    global _MODEL
    X = df[["quantity", "unit_price"]]
    y = df["total"]
    m = LinearRegression().fit(X, y)
    _MODEL = m
    return {
        "r2": float(m.score(X, y)),
        "coef": [float(c) for c in m.coef_.tolist()],
        "intercept": float(m.intercept_),
    }

def predict(quantity: int, unit_price: float) -> float:
    global _MODEL
    if _MODEL is None:
        df = load_sales_df()
        train_model(df)
    assert _MODEL is not None  # for type checker
    return float(_MODEL.predict([[quantity, unit_price]])[0])  # type: ignore[arg-type]
