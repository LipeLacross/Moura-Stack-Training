from __future__ import annotations
from fastapi import APIRouter
from app.backend.models import PredictRequest, PredictResponse
from app.services.data import load_sales_df, train_model, predict as predict_value

router = APIRouter(prefix="/ml", tags=["ml"])

@router.post("/train")
def train():  # type: ignore[override]
    df = load_sales_df()
    metrics = train_model(df)
    return metrics

@router.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest) -> PredictResponse:  # type: ignore[override]
    y_pred = predict_value(req.quantity, req.unit_price)
    return PredictResponse(y_pred=y_pred)
