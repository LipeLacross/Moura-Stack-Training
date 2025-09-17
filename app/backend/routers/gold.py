from __future__ import annotations
from fastapi import APIRouter
import os
import pandas as pd
from pathlib import Path

router = APIRouter(prefix="/gold", tags=["gold"])

@router.post("/export")
def export_gold():
    parquet_path = os.getenv("ETL_GOLD_PARQUET", "data/processed/sales.parquet")
    csv_path = os.getenv("ETL_GOLD_CSV", "data/processed/sales_gold.csv")
    p = Path(parquet_path)

    if not p.exists():
        # se ainda não existe, não falha: apenas informa
        return {"status": "no_parquet", "message": f"{parquet_path} não encontrado. Rode /etl/run primeiro."}

    df = pd.read_parquet(parquet_path)
    Path(csv_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(csv_path, index=False)
    return {"status": "ok", "rows": len(df), "parquet": parquet_path, "csv": csv_path}
