from __future__ import annotations
from fastapi import APIRouter
from app.backend.models import HealthCheck
from app.backend.db import ping

router = APIRouter(prefix="/health", tags=["health"])

@router.get("", response_model=HealthCheck)
def health() -> HealthCheck:
    return HealthCheck(status="ok", version="1.2.0", db_ok=ping())
