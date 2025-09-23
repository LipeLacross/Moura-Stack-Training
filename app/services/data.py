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
