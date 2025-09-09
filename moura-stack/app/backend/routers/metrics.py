from __future__ import annotations
from fastapi import APIRouter, HTTPException
from app.backend.models import SalesResponse, MetricSummary, SalesRecord
import pandas as pd
import numpy as np
from pathlib import Path
import os
from sqlalchemy import text
from app.backend.db import engine

router = APIRouter(prefix="/metrics", tags=["metrics"])

DATA_PATH = Path("data") / "sample_sales.csv"

def _load_df() -> pd.DataFrame:
    source = os.getenv("ETL_SOURCE", "csv")
    if source == "postgres":
        with engine.connect() as conn:
            df = pd.read_sql(text("SELECT order_id, region, product, quantity, unit_price, total FROM sales ORDER BY order_id"), conn)
    else:
        if not DATA_PATH.exists():
            raise HTTPException(status_code=500, detail="Sample dataset not found.")
        df = pd.read_csv(DATA_PATH)
        df["total"] = df["quantity"] * df["unit_price"]
    df["quantity"] = df["quantity"].astype(int)
    df["unit_price"] = df["unit_price"].astype(float)
    df["total"] = df["total"].astype(float)
    return df

@router.get("/sales", response_model=SalesResponse)
def list_sales(limit: int = 20) -> SalesResponse:
    df = _load_df()
    prev = df.head(limit).to_dict(orient="records")
    return SalesResponse(rows=len(df), preview=[SalesRecord(**r) for r in prev])

@router.get("/summary", response_model=MetricSummary)
def summary() -> MetricSummary:
    df = _load_df()
    total_revenue = float(df["total"].sum())
    total_quantity = int(df["quantity"].sum())
    avg_ticket = float(np.round(total_revenue / max(len(df), 1), 2))
    top_products = (
        df.groupby("product")["total"].sum().sort_values(ascending=False).head(5).index.tolist()
    )
    regions = sorted(df["region"].unique().tolist())
    return MetricSummary(
        total_revenue=total_revenue,
        total_quantity=total_quantity,
        avg_ticket=avg_ticket,
        top_products=top_products,
        regions=regions,
    )
