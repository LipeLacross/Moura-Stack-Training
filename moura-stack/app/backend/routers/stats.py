from __future__ import annotations
from fastapi import APIRouter, HTTPException
from app.backend.models import PearsonResponse, OLSResponse
import pandas as pd
from pathlib import Path
from scipy import stats
import statsmodels.api as sm
import os
from sqlalchemy import text
from app.backend.db import engine

router = APIRouter(prefix="/stats", tags=["stats"])
DATA_PATH = Path("data") / "sample_sales.csv"

def _load_df() -> pd.DataFrame:
    source = os.getenv("ETL_SOURCE", "csv")
    if source == "postgres":
        with engine.connect() as conn:
            df = pd.read_sql(text("SELECT quantity, unit_price, (quantity*unit_price) AS total FROM sales"), conn)
    else:
        if not DATA_PATH.exists():
            raise HTTPException(status_code=500, detail="Sample dataset not found.")
        df = pd.read_csv(DATA_PATH)
        df["total"] = df["quantity"] * df["unit_price"]
    df["quantity"] = df["quantity"].astype(int)
    df["unit_price"] = df["unit_price"].astype(float)
    df["total"] = df["total"].astype(float)
    return df

@router.get("/pearson", response_model=PearsonResponse)
def pearson_quantity_price() -> PearsonResponse:
    df = _load_df()
    r, p = stats.pearsonr(df["quantity"], df["unit_price"])
    return PearsonResponse(pearson_r=float(r), p_value=float(p))

@router.get("/ols", response_model=OLSResponse)
def ols_total_on_features() -> OLSResponse:
    df = _load_df()
    X = df[["quantity", "unit_price"]]
    X = sm.add_constant(X)
    y = df["total"]
    model = sm.OLS(y, X).fit()
    params = {k: float(v) for k, v in model.params.items()}
    return OLSResponse(params=params, r2=float(model.rsquared))
