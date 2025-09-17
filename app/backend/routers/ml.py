from __future__ import annotations
from fastapi import APIRouter
import os
import pandas as pd
from sqlalchemy import text
from app.backend.db import engine
from app.backend.models import PredictRequest, PredictResponse

from sklearn.linear_model import LinearRegression

router = APIRouter(prefix="/ml", tags=["ml"])

_MODEL: LinearRegression | None = None

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

@router.post("/train")
def train():
    global _MODEL
    df = _load_df()
    X = df[["quantity", "unit_price"]]
    y = df["total"]
    model = LinearRegression()
    model.fit(X, y)
    _MODEL = model
    r2 = float(model.score(X, y))
    coef = [float(c) for c in model.coef_.tolist()]
    intercept = float(model.intercept_)
    return {"r2": r2, "coef": coef, "intercept": intercept}

@router.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest) -> PredictResponse:  # type: ignore[override]
    global _MODEL
    if _MODEL is None:
        # fit rápido com os dados atuais
        df = _load_df()
        X = df[["quantity", "unit_price"]]
        y = df["total"]
        m = LinearRegression().fit(X, y)
        _MODEL = m
    y_pred = float(_MODEL.predict([[req.quantity, req.unit_price]])[0])  # type: ignore[arg-type]
    return PredictResponse(y_pred=y_pred)
