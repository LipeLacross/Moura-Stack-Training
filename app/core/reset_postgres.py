import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

def test_postgres_connection(db_url):
    try:
        engine = create_engine(db_url)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except OperationalError as e:
        print(f"[ERROR] Não foi possível conectar ao Postgres: {e}\nVerifique se o serviço está rodando e se a string de conexão está correta.")
        return False

def run_postgres_reset():
    db_url = os.getenv("DATABASE_URL", "")
    if not db_url or not test_postgres_connection(db_url):
        print("Abortando reset: conexão com Postgres indisponível ou DATABASE_URL não definida.")
        return
    engine = create_engine(db_url)
    sql_path = os.path.join(os.path.dirname(__file__), '../../sql/02_reset_sales.sql')
    with open(sql_path, 'r', encoding='utf-8') as f:
        sql_script = f.read()
    with engine.connect() as conn:
        for stmt in sql_script.split(';'):
            if stmt.strip():
                try:
                    conn.execute(text(stmt))
                except Exception as e:
                    print(f"Erro ao executar comando SQL: {e}\nComando: {stmt.strip()[:100]}")
    print("Banco Postgres resetado e populado com dados de exemplo.")

def check_date_column():
    db_url = os.getenv("DATABASE_URL", "")
    engine = create_engine(db_url)
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""SELECT column_name FROM information_schema.columns WHERE table_name='sales' AND column_name='date'"""))
            if result.fetchone():
                print("Coluna 'date' existe na tabela 'sales'. Reset OK.")
            else:
                print("Coluna 'date' NÃO existe na tabela 'sales'. Reset FALHOU.")
    except OperationalError as e:
        print(f"[ERROR] Não foi possível conectar ao Postgres para verificação: {e}")

if __name__ == "__main__":
    run_postgres_reset()
    check_date_column()
