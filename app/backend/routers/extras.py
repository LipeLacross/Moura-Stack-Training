from __future__ import annotations
from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
import io, base64
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

@router.get("/matplotlib-sales")
def matplotlib_sales():
    df = load_sales_df()
    fig, ax = plt.subplots(figsize=(7,4))
    df.groupby("product")['total'].sum().plot(kind='bar', ax=ax, color='skyblue')
    ax.set_title("Receita por Produto (Matplotlib)")
    buf = io.BytesIO()
    plt.tight_layout()
    fig.savefig(buf, format='png')
    plt.close(fig)
    img_b64 = base64.b64encode(buf.getvalue()).decode()
    return {"image": f"data:image/png;base64,{img_b64}"}

@router.get("/seaborn-sales")
def seaborn_sales():
    df = load_sales_df()
    plt.figure(figsize=(7,4))
    sns.barplot(data=df, x="product", y="total", hue="region")
    plt.title("Receita por Produto (Seaborn)")
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    plt.close()
    img_b64 = base64.b64encode(buf.getvalue()).decode()
    return {"image": f"data:image/png;base64,{img_b64}"}

@router.get("/ml/linear-regression")
def linear_regression():
    df = load_sales_df()
    # Exemplo: prever receita total a partir da quantidade
    X = df[["quantity"]]
    y = df["total"]
    from sklearn.linear_model import LinearRegression
    model = LinearRegression().fit(X, y)
    score = model.score(X, y)
    coef = model.coef_[0]
    intercept = model.intercept_
    # Previsão para quantidade média
    mean_qty = np.mean(df["quantity"])
    pred = model.predict([[mean_qty]])[0]
    return {
        "coef": coef,
        "intercept": intercept,
        "score": score,
        "mean_quantity": mean_qty,
        "predicted_total": pred
    }

@router.get("/bigdata/spark-aggregates")
def spark_aggregates():
    from pyspark.sql import SparkSession
    import pandas as pd
    df = load_sales_df()
    spark = SparkSession.builder.master("local[*]").appName("SalesAgg").getOrCreate()
    sdf = spark.createDataFrame(df)
    agg = sdf.groupBy("product").sum("total").toPandas()
    spark.stop()
    # Renomeia coluna para clareza
    agg = agg.rename(columns={"sum(total)": "total_revenue"})
    return agg.to_dict(orient="records")
