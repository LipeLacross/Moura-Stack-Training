from __future__ import annotations
from fastapi import APIRouter
from app.backend.routers.flow_etl import etl_sales

router = APIRouter(prefix="/etl", tags=["etl"])

@router.post("/run")
def run_etl():
    res = etl_sales()
    return {"status": "ok", "result": res}
