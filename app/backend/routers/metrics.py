from __future__ import annotations
from fastapi import APIRouter, Query
from typing import List
import os
import pandas as pd
from sqlalchemy import text
from app.backend.db import engine
from app.backend.models import SalesRecord, SalesResponse, MetricSummary

router = APIRouter(prefix="/metrics", tags=["metrics"])

def _load_df() -> pd.DataFrame:
    source = os.getenv("ETL_SOURCE", "csv")
    if source == "postgres":
        with engine.connect() as conn:
            df = pd.read_sql(
                text("SELECT order_id, region, product, quantity, unit_price, COALESCE(total, quantity*unit_price) AS total FROM sales ORDER BY order_id"),
                conn,
            )
    else:
        csv_path = os.getenv("ETL_CSV_PATH", "data/sample_sales.csv")
        df = pd.read_csv(csv_path)
        if "total" not in df.columns:
            df["total"] = df["quantity"] * df["unit_price"]
    return df

@router.get("/sales", response_model=SalesResponse)
def sales(limit: int = Query(100, ge=1, le=10_000)) -> SalesResponse:  # type: ignore[override]
    df = _load_df()
    if "order_id" in df.columns:
        df = df.sort_values("order_id")
    prev = df.head(limit).to_dict(orient="records")
    # garantir tipos coerentes com SalesRecord
    preview: List[SalesRecord] = [SalesRecord(**r) for r in prev]  # type: ignore[arg-type]
    return SalesResponse(rows=len(df), preview=preview)

@router.get("/summary", response_model=MetricSummary)
def summary() -> MetricSummary:  # type: ignore[override]
    df = _load_df()
    total_revenue = float(df["total"].sum()) if not df.empty else 0.0
    total_quantity = int(df["quantity"].sum()) if not df.empty else 0
    avg_ticket = float(df["total"].mean()) if not df.empty else 0.0
    top_products = (
        df.groupby("product")["total"].sum().sort_values(ascending=False).head(5).index.tolist()
        if not df.empty else []
    )
    regions = sorted(df["region"].dropna().unique().tolist()) if "region" in df.columns else []
    return MetricSummary(
        total_revenue=total_revenue,
        total_quantity=total_quantity,
        avg_ticket=avg_ticket,
        top_products=top_products,
        regions=regions,
    )
