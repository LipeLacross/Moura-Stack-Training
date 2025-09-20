import os
from sqlalchemy import text
from app.backend.db import engine


def log(msg: str):
    print(f"[DB INIT] {msg}")


def table_exists(table_name: str = "sales") -> bool:
    with engine.connect() as conn:
        result = conn.execute(text(f"""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' AND table_name = '{table_name}'
            )
        """))
        return result.scalar()


def get_db_info():
    with engine.connect() as conn:
        db = conn.execute(text("SELECT current_database()"))
        schema = conn.execute(text("SELECT current_schema()"))
        return db.scalar(), schema.scalar()


def init_db_if_needed():
    """
    Inicializa o banco executando o SQL de 02_reset_sales.sql se a tabela 'sales' não existir ou estiver com schema incorreto.
    Pode ser desabilitado via DB_AUTO_INIT=false.
    """
    auto_init = os.getenv("DB_AUTO_INIT", "true").lower() == "true"
    if not auto_init:
        log("Inicialização automática desabilitada.")
        return
    try:
        db_name, schema_name = get_db_info()
        log(f"Conectado ao banco: {db_name}, schema: {schema_name}")
        # Verifica se a tabela existe e se tem a coluna 'date'
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT column_name FROM information_schema.columns WHERE table_name = 'sales' AND column_name = 'date'
            """))
            has_date = result.rowcount > 0
        if not table_exists() or not has_date:
            log("Tabela 'sales' não existe ou está com schema incorreto. Executando 02_reset_sales.sql...")
            sql_path = os.path.join(os.path.dirname(__file__), '../../sql/02_reset_sales.sql')
            with open(sql_path, 'r', encoding='utf-8') as f:
                sql_script = f.read()
            with engine.connect() as conn:
                for stmt in sql_script.split(';'):
                    if stmt.strip():
                        conn.execute(text(stmt))
            log("Banco formatado e populado com dados de exemplo.")
        else:
            log("Tabela 'sales' já existe e está correta.")
    except Exception as e:
        log(f"Erro ao inicializar banco: {e}")


def reset_db_once():
    """
    Reseta o banco apenas se a tabela 'sales' não existir ou estiver vazia.
    Executa o script completo de reset (DROP TABLE + CREATE TABLE + INSERT).
    """
    auto_reset = os.getenv("DB_AUTO_RESET", "true").lower() == "true"
    if not auto_reset:
        log("Reset automático desabilitado.")
        return
    try:
        with engine.connect() as conn:
            # Verifica se a tabela existe
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' AND table_name = 'sales'
                )
            """))
            exists = result.scalar()
            # Verifica se está vazia
            empty = True
            if exists:
                count = conn.execute(text("SELECT COUNT(*) FROM sales")).scalar()
                empty = (count == 0)
            if not exists or empty:
                log("Resetando banco: executando 01_init.sql...")
                sql_path = os.path.join(os.path.dirname(__file__), '../../sql/01_init.sql')
                with open(sql_path, 'r', encoding='utf-8') as f:
                    sql_script = f.read()
                for stmt in sql_script.split(';'):
                    if stmt.strip():
                        conn.execute(text(stmt))
                log("Banco resetado e populado com dados de exemplo.")
            else:
                log("Banco já inicializado, não será resetado novamente.")
    except Exception as e:
        log(f"Erro ao resetar banco: {e}")
