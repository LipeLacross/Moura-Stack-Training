from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import processes, ml, llm, integration

app = FastAPI(
    title="Moura TI - API de Automação e Análise",
    description="API REST para automação de processos, ML, LLM e integração entre sistemas",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(processes.router, prefix="/api/processes", tags=["Processos"])
app.include_router(ml.router, prefix="/api/ml", tags=["Machine Learning"])
app.include_router(llm.router, prefix="/api/llm", tags=["LLM / IA Generativa"])
app.include_router(integration.router, prefix="/api/integration", tags=["Integração"])


@app.get("/health")
def health():
    return {"status": "ok", "service": "Moura TI API", "version": "1.0.0"}


@app.get("/")
def root():
    return {
        "message": "Moura TI - API de Automação e Análise",
        "docs": "/docs",
        "health": "/health",
    }
