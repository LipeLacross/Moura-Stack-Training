from __future__ import annotations
from fastapi import APIRouter, Query
from typing import List
import pandas as pd
from app.backend.models import SalesRecord, SalesResponse, MetricSummary
from app.services.data import load_sales_df, compute_summary

router = APIRouter(prefix="/metrics", tags=["metrics"])

@router.get("/sales", response_model=SalesResponse)
def sales(
    limit: int = Query(100, ge=1, le=10_000),
    offset: int = Query(0, ge=0),
    start_date: str = Query(None, description="Data inicial (YYYY-MM-DD)"),
    end_date: str = Query(None, description="Data final (YYYY-MM-DD)"),
    product: str = Query(None, description="Produto")
) -> SalesResponse:  # type: ignore[override]
    df: pd.DataFrame = load_sales_df(start_date=start_date, end_date=end_date, product=product)
    if "order_id" in df.columns:
        df = df.sort_values("order_id")
    prev = df.iloc[offset:offset+limit].to_dict(orient="records")
    # Conversão robusta de campos de data/hora para string
    for r in prev:
        for field in ["date", "created_at", "updated_at"]:
            val = r.get(field)
            if val is None or (hasattr(val, 'isnull') and val.isnull()):
                r[field] = None
            elif hasattr(val, 'isoformat'):
                r[field] = val.isoformat()
            else:
                r[field] = str(val) if val else None
    # garantir tipos coerentes com SalesRecord
    preview: List[SalesRecord] = [SalesRecord(**r) for r in prev]  # type: ignore[arg-type]
    return SalesResponse(rows=len(df), preview=preview)

@router.get("/summary", response_model=MetricSummary)
def summary(
    start_date: str = Query(None, description="Data inicial (YYYY-MM-DD)"),
    end_date: str = Query(None, description="Data final (YYYY-MM-DD)"),
    product: str = Query(None, description="Produto")
) -> MetricSummary:  # type: ignore[override]
    df = load_sales_df(start_date=start_date, end_date=end_date, product=product)
    sm = compute_summary(df)
    return MetricSummary(**sm)
