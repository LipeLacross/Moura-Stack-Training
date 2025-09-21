from __future__ import annotations
from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
import io, base64
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from app.services.data import load_sales_df
from app.backend.routers.spark_job import run_spark_job

router = APIRouter(prefix="", tags=["extras"])

@router.get("/export/excel", response_class=StreamingResponse)
def export_excel():  # type: ignore[override]
    df = load_sales_df()
    output = io.BytesIO()
    df.to_excel(output, index=False, engine="openpyxl")
    output.seek(0)
    headers = {"Content-Disposition": "attachment; filename=sales.xlsx"}
    return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers=headers)

@router.post("/spark/run")
def spark_run():  # type: ignore[override]
    res = run_spark_job()
    return JSONResponse(res)

@router.get("/plotly-sales")
def plotly_sales():
    df = load_sales_df()
    fig = px.bar(df, x="product", y="total", color="region", title="Receita por Produto (Plotly)")
    return fig.to_json()

def get_sales_df():
    df = load_sales_df()
    # Garante coluna 'total' para todos os endpoints
    if 'total' not in df.columns and 'quantity' in df.columns and 'unit_price' in df.columns:
        df['total'] = df['quantity'] * df['unit_price']
    return df

@router.get("/matplotlib-sales")
def matplotlib_sales():
    try:
        df = get_sales_df()
        if df.empty or 'product' not in df or 'total' not in df:
            return {"image": None, "error": "No data available for Matplotlib chart."}
        fig, ax = plt.subplots(figsize=(7,4))
        df.groupby("product")['total'].sum().plot(kind='bar', ax=ax, color='skyblue')
        ax.set_title("Receita por Produto (Matplotlib)")
        buf = io.BytesIO()
        plt.tight_layout()
        fig.savefig(buf, format='png')
        plt.close(fig)
        img_b64 = base64.b64encode(buf.getvalue()).decode()
        return {"image": f"data:image/png;base64,{img_b64}"}
    except Exception as e:
        return {"image": None, "error": f"Matplotlib error: {str(e)}"}

@router.get("/seaborn-sales")
def seaborn_sales():
    try:
        df = get_sales_df()
        if df.empty or 'product' not in df or 'total' not in df or 'region' not in df:
            return {"image": None, "error": "No data available for Seaborn chart."}
        plt.figure(figsize=(7,4))
        sns.barplot(data=df, x="product", y="total", hue="region")
        plt.title("Receita por Produto (Seaborn)")
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png')
        plt.close()
        img_b64 = base64.b64encode(buf.getvalue()).decode()
        return {"image": f"data:image/png;base64,{img_b64}"}
    except Exception as e:
        return {"image": None, "error": f"Seaborn error: {str(e)}"}

@router.get("/ml/linear-regression")
def linear_regression():
    try:
        df = get_sales_df()
        if df.empty or 'quantity' not in df or 'total' not in df:
            return {"error": "No data available for regression."}
        X = df[["quantity"]]
        y = df["total"]
        from sklearn.linear_model import LinearRegression
        model = LinearRegression().fit(X, y)
        score = model.score(X, y)
        coef = model.coef_[0]
        intercept = model.intercept_
        mean_qty = float(np.mean(df["quantity"]))
        pred = float(model.predict([[mean_qty]])[0])
        return {
            "coef": coef,
            "intercept": intercept,
            "score": score,
            "mean_quantity": mean_qty,
            "predicted_total": pred
        }
    except Exception as e:
        return {"error": f"Regression error: {str(e)}"}

@router.get("/bigdata/spark-aggregates")
def spark_aggregates():
    try:
        df = get_sales_df()
        if df.empty or 'product' not in df or 'total' not in df:
            return []
        from pyspark.sql import SparkSession
        spark = SparkSession.builder.master("local[*]").appName("SalesAgg").getOrCreate()
        sdf = spark.createDataFrame(df)
        agg = sdf.groupBy("product").sum("total").toPandas()
        spark.stop()
        agg = agg.rename(columns={"sum(total)": "total_revenue"})
        return agg.to_dict(orient="records")
    except Exception as e:
        return [{"product": None, "total_revenue": None, "error": f"PySpark error: {str(e)}"}]
