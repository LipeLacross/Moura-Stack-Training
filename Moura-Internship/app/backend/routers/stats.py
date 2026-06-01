from __future__ import annotations
from fastapi import APIRouter
from app.backend.models import PearsonResponse, OLSResponse
from app.services.data import load_sales_df, compute_pearson, compute_ols

router = APIRouter(prefix="/stats", tags=["stats"])

@router.get("/pearson", response_model=PearsonResponse)
def pearson() -> PearsonResponse:  # type: ignore[override]
    df = load_sales_df()
    res = compute_pearson(df)
    return PearsonResponse(**res)

@router.get("/ols", response_model=OLSResponse)
def ols() -> OLSResponse:  # type: ignore[override]
    df = load_sales_df()
    res = compute_ols(df)
    return OLSResponse(**res)
