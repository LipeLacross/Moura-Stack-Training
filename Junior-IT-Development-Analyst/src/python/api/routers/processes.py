from fastapi import APIRouter, HTTPException
from ..models import ProcessFlow

router = APIRouter()

_processes_db: list[ProcessFlow] = []


@router.get("/", response_model=list[ProcessFlow])
def list_processes():
    return _processes_db


@router.post("/", response_model=ProcessFlow, status_code=201)
def create_process(flow: ProcessFlow):
    from datetime import datetime
    flow.id = len(_processes_db) + 1
    flow.created_at = datetime.now()
    flow.updated_at = datetime.now()
    _processes_db.append(flow)
    return flow


@router.get("/{process_id}", response_model=ProcessFlow)
def get_process(process_id: int):
    for p in _processes_db:
        if p.id == process_id:
            return p
    raise HTTPException(404, "Processo não encontrado")


@router.put("/{process_id}", response_model=ProcessFlow)
def update_process(process_id: int, flow: ProcessFlow):
    from datetime import datetime
    for i, p in enumerate(_processes_db):
        if p.id == process_id:
            flow.id = process_id
            flow.created_at = p.created_at
            flow.updated_at = datetime.now()
            _processes_db[i] = flow
            return flow
    raise HTTPException(404, "Processo não encontrado")


@router.delete("/{process_id}", status_code=204)
def delete_process(process_id: int):
    for i, p in enumerate(_processes_db):
        if p.id == process_id:
            _processes_db.pop(i)
            return
    raise HTTPException(404, "Processo não encontrado")
