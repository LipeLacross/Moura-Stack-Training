from fastapi import APIRouter, HTTPException
from ..models import IntegrationRequest, IntegrationResponse
import hashlib
import json
from datetime import datetime

router = APIRouter()

_sync_log: list[dict] = []


@router.post("/sync", response_model=IntegrationResponse)
def sync_systems(request: IntegrationRequest):
    sync_id = hashlib.md5(
        f"{request.source_system}:{request.target_system}:{datetime.now().isoformat()}".encode()
    ).hexdigest()[:12]

    records = []

    if isinstance(request.payload, dict):
        if "items" in request.payload:
            records = request.payload["items"]
        elif isinstance(request.payload, list):
            records = request.payload
        else:
            records = [request.payload]

    _sync_log.append({
        "sync_id": sync_id,
        "source": request.source_system,
        "target": request.target_system,
        "action": request.action,
        "records": len(records),
        "timestamp": datetime.now().isoformat(),
    })

    return IntegrationResponse(
        status="success",
        message=f"Sincronização de {request.source_system} para {request.target_system} concluída",
        sync_id=sync_id,
        records_processed=len(records),
    )


@router.get("/sync/history")
def sync_history():
    return _sync_log


@router.get("/systems")
def list_systems():
    return {
        "available": [
            {"id": "sap", "name": "SAP ERP", "protocols": ["RFC", "BAPI"]},
            {"id": "powerbi", "name": "Power BI", "protocols": ["REST", "Embed"]},
            {"id": "azure-boards", "name": "Azure Boards", "protocols": ["REST API"]},
            {"id": "sql-database", "name": "Banco SQL", "protocols": ["ODBC", "SQLAlchemy"]},
            {"id": "external-api", "name": "API Externa", "protocols": ["REST", "Webhook"]},
        ]
    }
