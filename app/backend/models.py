from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Dict

class SalesRecord(BaseModel):
    order_id: int = Field(..., ge=1)
    region: str
    product: str
    quantity: int = Field(..., ge=0)
    unit_price: float = Field(..., ge=0)
    total: float = Field(..., ge=0)
    date: str
    customer_id: int | None = None
    status: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    notes: str | None = None
    user_id: int | None = None
    category: str | None = None
    payment_method: str | None = None

class SalesResponse(BaseModel):
    rows: int
    preview: List[SalesRecord]

class MetricSummary(BaseModel):
    total_revenue: float
    total_quantity: int
    avg_ticket: float
    top_products: List[str]
    regions: List[str]

class HealthCheck(BaseModel):
    status: str
    version: str
    db_ok: bool

class PearsonResponse(BaseModel):
    pearson_r: float
    p_value: float

class OLSResponse(BaseModel):
    params: Dict[str, float]
    r2: float

class PredictRequest(BaseModel):
    quantity: int = Field(..., ge=0)
    unit_price: float = Field(..., ge=0)

class PredictResponse(BaseModel):
    y_pred: float
