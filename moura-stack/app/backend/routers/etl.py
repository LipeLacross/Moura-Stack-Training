from __future__ import annotations
from fastapi import APIRouter
from app.etl.flow_etl import etl_sales

router = APIRouter(prefix="/etl", tags=["etl"])

@router.post("/run")
def run_etl() -> dict:
    """
    Endpoint tipo webhook para ser chamado pelo Power Automate.
    Executa o flow do Prefect sincronicamente (demo).
    """
    etl_sales()  # executa com defaults de env
    return {"status": "ok", "message": "ETL disparado"}
