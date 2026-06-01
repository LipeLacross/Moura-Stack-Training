from fastapi import APIRouter, HTTPException
from ..models import LLMRequest, LLMResponse
import os

router = APIRouter()


@router.post("/generate", response_model=LLMResponse)
def generate_text(request: LLMRequest):
    try:
        from ...llm.client import LLMClient
        client = LLMClient(
            api_key=os.getenv("LLM_API_KEY", ""),
            endpoint=os.getenv("LLM_ENDPOINT", "https://api.openai.com/v1"),
            model=os.getenv("LLM_MODEL", "gpt-4o-mini"),
        )
        result = client.generate(
            prompt=request.prompt,
            system_context=request.system_context,
            temperature=request.temperature,
        )
        return LLMResponse(**result)
    except Exception as e:
        raise HTTPException(500, f"Erro ao gerar texto: {str(e)}")


@router.post("/analyze-sentiment")
def analyze_sentiment(texts: list[str]):
    try:
        from ...llm.prompts import SentimentAnalyzer
        analyzer = SentimentAnalyzer()
        results = analyzer.analyze_batch(texts)
        return {"results": results}
    except Exception as e:
        raise HTTPException(500, f"Erro na análise de sentimento: {str(e)}")


@router.post("/generate-report")
def generate_report(data_summary: dict):
    try:
        from ...llm.generators import ReportGenerator
        gen = ReportGenerator()
        report = gen.generate_technical_report(data_summary)
        return {"report": report}
    except Exception as e:
        raise HTTPException(500, f"Erro ao gerar relatório: {str(e)}")
