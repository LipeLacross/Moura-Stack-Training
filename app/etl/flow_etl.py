from __future__ import annotations
from prefect import flow, task
import pandas as pd
from pathlib import Path
import os
from sqlalchemy import text
from app.backend.db import engine

@task
def extract_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

@task
def extract_postgres() -> pd.DataFrame:
    with engine.connect() as conn:
        return pd.read_sql(text("SELECT order_id, region, product, quantity, unit_price FROM sales ORDER BY order_id"), conn)

@task
def transform(df: pd.DataFrame) -> pd.DataFrame:
    df["total"] = df["quantity"] * df["unit_price"]
    return df

@task
def load_parquet(df: pd.DataFrame, out_path: str) -> None:
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out_path, index=False)

@flow(name="moura-etl")
def etl_sales(
    src: str | None = None,
    dest: str | None = None,
):
    source = os.getenv("ETL_SOURCE", "csv")
    csv_path = src or os.getenv("ETL_CSV_PATH", "data/sample_sales.csv")
    out_path = dest or os.getenv("ETL_GOLD_PARQUET", "data/processed/sales.parquet")
    if source == "postgres":
        df = extract_postgres()
    else:
        df = extract_csv(csv_path)
    tdf = transform(df)
    load_parquet(tdf, out_path)
    return {"rows": len(tdf), "dest": out_path}

if __name__ == "__main__":
    etl_sales()
