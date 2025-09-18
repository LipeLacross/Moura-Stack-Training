from __future__ import annotations
import os
from typing import Dict, Any, List
import pandas as pd
from sqlalchemy import text
from app.backend.db import engine
from sklearn.linear_model import LinearRegression
from scipy.stats import pearsonr
import statsmodels.api as sm

_MODEL: LinearRegression | None = None

# TODO(refactor, 2025-09-18, consolidar validações de schema se dado crescer)

def load_sales_df() -> pd.DataFrame:
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

def compute_summary(df: pd.DataFrame) -> Dict[str, Any]:
    if df.empty:
        return {
            "total_revenue": 0.0,
            "total_quantity": 0,
            "avg_ticket": 0.0,
            "top_products": [],
            "regions": [],
        }
    total_revenue = float(df["total"].sum())
    total_quantity = int(df["quantity"].sum())
    avg_ticket = float(df["total"].mean())
    top_products = (
        df.groupby("product")["total"].sum().sort_values(ascending=False).head(5).index.tolist()
    )
    regions = sorted(df["region"].dropna().unique().tolist()) if "region" in df.columns else []
    return {
        "total_revenue": total_revenue,
        "total_quantity": total_quantity,
        "avg_ticket": avg_ticket,
        "top_products": top_products,
        "regions": regions,
    }

def compute_pearson(df: pd.DataFrame) -> Dict[str, float]:
    r, p = pearsonr(df["quantity"], df["unit_price"])
    return {"pearson_r": float(r), "p_value": float(p)}

def compute_ols(df: pd.DataFrame) -> Dict[str, Any]:
    y = df["total"]
    X = df[["quantity", "unit_price"]]
    X = sm.add_constant(X, prepend=True)
    model = sm.OLS(y, X).fit()
    params = {k: float(v) for k, v in model.params.to_dict().items()}
    return {"params": params, "r2": float(model.rsquared)}

def train_model(df: pd.DataFrame) -> Dict[str, Any]:
    global _MODEL
    X = df[["quantity", "unit_price"]]
    y = df["total"]
    m = LinearRegression().fit(X, y)
    _MODEL = m
    return {
        "r2": float(m.score(X, y)),
        "coef": [float(c) for c in m.coef_.tolist()],
        "intercept": float(m.intercept_),
    }

def predict(quantity: int, unit_price: float) -> float:
    global _MODEL
    if _MODEL is None:
        df = load_sales_df()
        train_model(df)
    assert _MODEL is not None  # for type checker
    return float(_MODEL.predict([[quantity, unit_price]])[0])  # type: ignore[arg-type]

