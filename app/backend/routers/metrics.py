from __future__ import annotations
from fastapi import APIRouter, Query
from typing import List
import pandas as pd
from app.backend.models import SalesRecord, SalesResponse, MetricSummary
from app.services.data import load_sales_df, compute_summary

router = APIRouter(prefix="/metrics", tags=["metrics"])

@router.get("/sales", response_model=SalesResponse)
def sales(limit: int = Query(100, ge=1, le=10_000)) -> SalesResponse:  # type: ignore[override]
    df: pd.DataFrame = load_sales_df()
    if "order_id" in df.columns:
        df = df.sort_values("order_id")
    prev = df.head(limit).to_dict(orient="records")
    # garantir tipos coerentes com SalesRecord
    preview: List[SalesRecord] = [SalesRecord(**r) for r in prev]  # type: ignore[arg-type]
    return SalesResponse(rows=len(df), preview=preview)

@router.get("/summary", response_model=MetricSummary)
def summary() -> MetricSummary:  # type: ignore[override]
    df = load_sales_df()
    sm = compute_summary(df)
    return MetricSummary(**sm)
