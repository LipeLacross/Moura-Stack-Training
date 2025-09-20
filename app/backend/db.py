from __future__ import annotations
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Usa apenas PostgreSQL, obtendo a string de conexão da variável de ambiente POSTGRES_URL
DATABASE_URL = os.getenv("POSTGRES_URL")
if not DATABASE_URL or not DATABASE_URL.strip():
    raise RuntimeError("POSTGRES_URL não definida. Configure a variável de ambiente com a string de conexão do Postgres.")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def ping() -> bool:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False
