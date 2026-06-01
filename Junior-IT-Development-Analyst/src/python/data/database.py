import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Optional

Base = declarative_base()

engine = None
SessionLocal = None


def get_engine(database_url: Optional[str] = None):
    global engine
    if engine is None:
        url = database_url or os.getenv("DATABASE_URL")
        if not url:
            raise ValueError("DATABASE_URL não configurada")
        engine = create_engine(url, pool_size=5, max_overflow=10)
    return engine


def get_session():
    global SessionLocal
    if SessionLocal is None:
        SessionLocal = sessionmaker(bind=get_engine())
    return SessionLocal()


def execute_query(sql: str, params: Optional[dict] = None) -> list[dict]:
    with get_session() as session:
        result = session.execute(text(sql), params or {})
        if result.returns_rows:
            columns = result.keys()
            return [dict(zip(columns, row)) for row in result.fetchall()]
        session.commit()
        return []


def test_connection() -> dict:
    try:
        with get_session() as session:
            session.execute(text("SELECT 1"))
            return {"status": "ok", "message": "Conexão estabelecida com sucesso"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
