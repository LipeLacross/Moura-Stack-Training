import os
from sqlalchemy import text
from app.backend.db import engine, IS_SQLITE


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
    if IS_SQLITE:
        return "sqlite", None
    else:
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
        log(f"Conectado ao banco: {db_name}")
        with engine.connect() as conn:
            if IS_SQLITE:
                result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='sales';"))
                table_exists = result.fetchone() is not None
                has_date = False
                if table_exists:
                    col_result = conn.execute(text("PRAGMA table_info(sales);"))
                    for row in col_result:
                        if row[1] == 'date':
                            has_date = True
                            break
            else:
                result = conn.execute(text("""
                    SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'sales'
                """))
                table_exists = result.scalar() > 0
                col_result = conn.execute(text("""
                    SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'sales' AND column_name = 'date'
                """))
                has_date = col_result.scalar() > 0
        if not table_exists or not has_date:
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


def ensure_sales_schema():
    """
    Garante que todas as colunas obrigatórias existem na tabela sales, corrigindo o schema automaticamente.
    """
    required_columns = [
        ('date', "DATE NOT NULL DEFAULT CURRENT_DATE"),
        ('customer_id', "INT"),
        ('status', "TEXT DEFAULT 'paid'"),
        ('created_at', "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"),
        ('updated_at', "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"),
        ('notes', "TEXT"),
        ('user_id', "INT"),
        ('category', "TEXT"),
        ('payment_method', "TEXT")
    ]
    with engine.connect() as conn:
        for col, coltype in required_columns:
            result = conn.execute(text(f"""
                SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'sales' AND column_name = '{col}'
            """))
            exists = result.scalar() > 0
            if not exists:
                try:
                    conn.execute(text(f"ALTER TABLE sales ADD COLUMN {col} {coltype};"))
                    log(f"Coluna '{col}' adicionada ao schema sales.")
                except Exception as e:
                    log(f"Erro ao adicionar coluna '{col}': {e}")


def reset_db_once():
    """
    Reseta o banco apenas se a tabela 'sales' não existir ou estiver vazia.
    Se a tabela existir mas estiver sem a coluna 'date', corrige o schema antes de qualquer operação.
    Executa o script completo de reset (DROP TABLE + CREATE TABLE + INSERT).
    """
    auto_reset = os.getenv("DB_AUTO_RESET", "true").lower() == "true"
    if not auto_reset:
        log("Reset automático desabilitado.")
        return
    try:
        with engine.connect() as conn:
            if IS_SQLITE:
                result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='sales';"))
                exists = result.fetchone() is not None
                empty = True
                if exists:
                    count = conn.execute(text("SELECT COUNT(*) FROM sales;")).scalar()
                    empty = (count == 0)
                    col_result = conn.execute(text("PRAGMA table_info(sales);"))
                    has_date = False
                    for row in col_result:
                        if row[1] == 'date':
                            has_date = True
                            break
                else:
                    has_date = False
            else:
                result = conn.execute(text("""
                    SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'sales'
                """))
                exists = result.scalar() > 0
                empty = True
                if exists:
                    count = conn.execute(text("SELECT COUNT(*) FROM sales;")).scalar()
                    empty = (count == 0)
                    col_result = conn.execute(text("""
                        SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'sales' AND column_name = 'date'
                    """))
                    has_date = col_result.scalar() > 0
                else:
                    has_date = False
            if not exists or empty or not has_date:
                log("Resetando banco: executando 02_reset_sales.sql...")
                sql_path = os.path.join(os.path.dirname(__file__), '../../sql/02_reset_sales.sql')
                with open(sql_path, 'r', encoding='utf-8') as f:
                    sql_script = f.read()
                for stmt in sql_script.split(';'):
                    if stmt.strip():
                        conn.execute(text(stmt))
                log("Banco resetado e populado com dados de exemplo.")
            else:
                log("Tabela 'sales' já existe, está correta e populada.")
    except Exception as e:
        log(f"Erro ao resetar banco: {e}")
