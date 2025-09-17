from fastapi import APIRouter
from app.backend.models import HealthCheck
from app.backend.db import ping

router = APIRouter(tags=["health"])

# Evitar import circular com app.main: fixamos a versão aqui igual à do main.py
API_VERSION = "1.2.0"

@router.get("/health", response_model=HealthCheck)
def health() -> HealthCheck:  # type: ignore[override]
    return HealthCheck(status="ok", version=API_VERSION, db_ok=ping())
