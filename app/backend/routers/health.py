from fastapi import APIRouter
from app.backend.models import HealthCheck
from app.backend.db import ping
import logging

router = APIRouter(tags=["health"])

# Evitar import circular com app.main: fixamos a versão aqui igual à do main.py
API_VERSION = "1.2.0"

@router.get("/health", response_model=HealthCheck)
def health() -> HealthCheck:  # type: ignore[override]
    db_ok = False
    try:
        db_ok = ping()
    except Exception as e:
        logging.error(f"[HEALTH] Erro ao pingar banco: {e}")
        db_ok = False
    return HealthCheck(status="ok", version=API_VERSION, db_ok=db_ok)
