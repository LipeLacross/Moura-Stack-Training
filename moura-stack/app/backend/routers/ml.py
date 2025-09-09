from __future__ import annotations
from fastapi import APIRouter, HTTPException
from app.backend.models import PredictRequest, PredictResponse
from pathlib import Path
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import os
from sqlalchemy import text
from app.backend.db import engine

router = APIRouter(prefix="/ml", tags=["ml"])

_model: LinearRegression | None = None
DATA_PATH = Path("data") / "sample_sales.csv"

def _load_df() -> pd.DataFrame:
    source = os.getenv("ETL_SOURCE", "csv")
    if source == "postgres":
        with engine.connect() as conn:
            df = pd.read_sql(text("SELECT quantity, unit_price, total FROM sales"), conn)
    else:
        if not DATA_PATH.exists():
            raise HTTPException(status_code=500, detail="Sample dataset not found.")
        df = pd.read_csv(DATA_PATH)
        df["total"] = df["quantity"] * df["unit_price"]
    df["quantity"] = df["quantity"].astype(int)
    df["unit_price"] = df["unit_price"].astype(float)
    df["total"] = df["total"].astype(float)
    return df

@router.post("/train")
def train_model() -> dict:
    global _model
    df = _load_df()
    X = df[["quantity", "unit_price"]].values
    y = df["total"].values
    _model = LinearRegression()
    _model.fit(X, y)
    r2 = float(_model.score(X, y))
    coefs = _model.coef_.tolist()
    intercept = float(_model.intercept_)
    return {"status": "trained", "r2": r2, "coef": coefs, "intercept": intercept}

@router.post("/predict", response_model=PredictResponse)
def predict(body: PredictRequest) -> PredictResponse:
    if _model is None:
        raise HTTPException(status_code=400, detail="Model not trained. Call /ml/train first.")
    X = np.array([[body.quantity, body.unit_price]])
    y_pred = float(_model.predict(X)[0])
    return PredictResponse(y_pred=y_pred)
