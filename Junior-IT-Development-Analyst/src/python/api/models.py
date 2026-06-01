from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime


class ProcessFlow(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    bpmn_xml: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class MLPredictionRequest(BaseModel):
    features: list[float] = Field(..., description="Vetor de features para predição")
    model_type: str = Field(..., pattern="^(classifier|regressor|cluster)$")


class MLPredictionResponse(BaseModel):
    prediction: Any
    probability: Optional[float] = None
    model_used: str
    feature_importance: Optional[dict[str, float]] = None


class LLMRequest(BaseModel):
    prompt: str
    system_context: Optional[str] = "Você é um assistente de TI especializado em automação e análise de dados."
    temperature: float = 0.7


class LLMResponse(BaseModel):
    content: str
    model: str
    tokens_used: int


class IntegrationRequest(BaseModel):
    source_system: str
    target_system: str
    payload: dict[str, Any]
    action: str = "sync"


class IntegrationResponse(BaseModel):
    status: str
    message: str
    sync_id: Optional[str] = None
    records_processed: Optional[int] = None


class ETLRequest(BaseModel):
    source: str = "csv"
    table_name: str
    batch_size: int = 10000


class ETLResponse(BaseModel):
    status: str
    rows_loaded: int
    duration_seconds: float
    target_table: str
