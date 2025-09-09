from __future__ import annotations
from fastapi import APIRouter
import os
import pandas as pd
from sqlalchemy import text
from app.backend.db import engine

router = APIRouter(prefix="/gold", tags=["gold"])

@router.post("/export")
def export_gold() -> dict:
    """
    Exporta camada 'gold' em Parquet e CSV para o Power BI consumir.
    Se ETL_SOURCE=postgres, lê da tabela `sales`. Caso contrário, do CSV.
    Paths controlados por env: ETL_GOLD_PARQUET, ETL_GOLD_CSV.
    """
    source = os.getenv("ETL_SOURCE", "csv")
    parquet_path = os.getenv("ETL_GOLD_PARQUET", "data/processed/sales.parquet")
    csv_path = os.getenv("ETL_GOLD_CSV", "data/processed/sales_gold.csv")

    if source == "postgres":
        with engine.connect() as conn:
            df = pd.read_sql(text("""
                SELECT order_id, region, product, quantity, unit_price, (quantity*unit_price) AS total
                FROM sales
                ORDER BY order_id
            """), conn)
    else:
        df = pd.read_csv("data/sample_sales.csv")
        df["total"] = df["quantity"] * df["unit_price"]

    # "gold": já limpo e pronto p/ BI
    df.to_parquet(parquet_path, index=False)
    df.to_csv(csv_path, index=False)
    return {"status": "ok", "parquet": parquet_path, "csv": csv_path, "rows": len(df)}
