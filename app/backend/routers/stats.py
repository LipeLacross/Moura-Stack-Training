from __future__ import annotations
from fastapi import APIRouter
import os
import pandas as pd
from sqlalchemy import text
from app.backend.db import engine
from app.backend.models import PearsonResponse, OLSResponse

from scipy.stats import pearsonr
import statsmodels.api as sm

router = APIRouter(prefix="/stats", tags=["stats"])

def _load_df() -> pd.DataFrame:
    source = os.getenv("ETL_SOURCE", "csv")
    if source == "postgres":
        with engine.connect() as conn:
            df = pd.read_sql(
                text("SELECT order_id, region, product, quantity, unit_price, COALESCE(total, quantity*unit_price) AS total FROM sales"),
                conn,
            )
    else:
        csv_path = os.getenv("ETL_CSV_PATH", "data/sample_sales.csv")
        df = pd.read_csv(csv_path)
        if "total" not in df.columns:
            df["total"] = df["quantity"] * df["unit_price"]
    return df

@router.get("/pearson", response_model=PearsonResponse)
def pearson() -> PearsonResponse:  # type: ignore[override]
    df = _load_df()
    r, p = pearsonr(df["quantity"], df["unit_price"])
    return PearsonResponse(pearson_r=float(r), p_value=float(p))

@router.get("/ols", response_model=OLSResponse)
def ols() -> OLSResponse:  # type: ignore[override]
    df = _load_df()
    y = df["total"]
    X = df[["quantity", "unit_price"]]
    X = sm.add_constant(X, prepend=True)
    model = sm.OLS(y, X).fit()
    params = {k: float(v) for k, v in model.params.to_dict().items()}
    return OLSResponse(params=params, r2=float(model.rsquared))
