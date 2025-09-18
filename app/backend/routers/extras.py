from __future__ import annotations
import io
from fastapi import APIRouter
from fastapi.responses import StreamingResponse, JSONResponse
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
