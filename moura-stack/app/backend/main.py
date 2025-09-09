from __future__ import annotations
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.backend.routers import health, metrics, stats, ml, etl, gold

app = FastAPI(title="Moura Stack API", version="1.2.0")

origins = [
    os.getenv("FRONTEND_ORIGIN", "http://localhost:8501"),
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(metrics.router)
app.include_router(stats.router)
app.include_router(ml.router)
app.include_router(etl.router)
app.include_router(gold.router)
