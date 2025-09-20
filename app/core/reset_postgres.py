import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from app.core.utils import log
import re

def test_postgres_connection(db_url):
    try:
        engine = create_engine(db_url)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except OperationalError as e:
        log(f"Não foi possível conectar ao Postgres: {e}\nVerifique se o serviço está rodando e se a string de conexão está correta.", level="ERROR")
        return False

def split_sql_blocks(sql_script):
    # Divide o script em blocos robustos: CREATE TABLE, FUNCTION, PROCEDURE, TRIGGER, INSERT
    pattern = r"(?<=;)(?=\s*CREATE|\s*DROP|\s*INSERT|\s*CALL|\s*ALTER|\s*DO|\s*--|$)"
    blocks = re.split(pattern, sql_script, flags=re.IGNORECASE)
    return [b.strip() for b in blocks if b.strip()]

def run_postgres_reset():
    db_url = os.getenv("DATABASE_URL", "")
    if not db_url or not test_postgres_connection(db_url):
        log("Abortando reset: conexão com Postgres indisponível ou DATABASE_URL não definida.", level="ERROR")
        return
    engine = create_engine(db_url)
    sql_path = os.path.join(os.path.dirname(__file__), '../../sql/02_reset_sales.sql')
    with open(sql_path, 'r', encoding='utf-8') as f:
        sql_script = f.read()
    blocks = split_sql_blocks(sql_script)
    with engine.connect() as conn:
        for block in blocks:
            try:
                conn.execute(text(block))
            except Exception as e:
                log(f"Erro ao executar bloco SQL: {e}\nBloco: {block[:120]}", level="ERROR")
    log("Banco Postgres resetado e populado com dados de exemplo.", level="INFO")

def check_date_column():
    db_url = os.getenv("DATABASE_URL", "")
    engine = create_engine(db_url)
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""SELECT column_name FROM information_schema.columns WHERE table_name='sales' AND column_name='date'"""))
            if result.fetchone():
                log("Coluna 'date' existe na tabela 'sales'. Reset OK.", level="INFO")
            else:
                log("Coluna 'date' NÃO existe na tabela 'sales'. Reset FALHOU.", level="WARNING")
    except OperationalError as e:
        log(f"Não foi possível conectar ao Postgres para verificação: {e}", level="ERROR")

if __name__ == "__main__":
    run_postgres_reset()
    check_date_column()
