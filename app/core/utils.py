import os
import re
from sqlalchemy import text
from app.backend.db import engine


def log(msg: str, level: str = "INFO"):
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    levels = ["ERROR", "WARNING", "INFO", "DEBUG"]
    if levels.index(level) <= levels.index(log_level):
        print(f"[{level}] {msg}")


def process_sql_script(sql_script: str) -> str:
    # Apenas remove CASCADE do DROP TABLE, mantendo o restante do script original
    sql_script = re.sub(r"DROP TABLE IF EXISTS ([^;]+) CASCADE", r"DROP TABLE IF EXISTS \1", sql_script)
    return sql_script


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
        log(f"Conectado ao banco: {db_name}")
        with engine.connect() as conn:
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
            log(f"[DEBUG] Script SQL lido:\n{sql_script[:500]}")
            sql_script = process_sql_script(sql_script)
            # Extract the CREATE TABLE sales statement for potential later use
            create_sales = re.search(r'(?s)CREATE TABLE sales\b.*?\)\s*;', sql_script, re.IGNORECASE)
            try:
                with engine.connect() as conn:
                    log("[DEBUG] Executando script SQL completo via cursor nativo...")
                    cursor = conn.connection.cursor()
                    cursor.execute(sql_script)
                    cursor.close()
                    log("[DEBUG] Script SQL completo executado.")
            except Exception as e:
                log(f"[ERRO] Falha ao executar script SQL completo: {e}")
            with engine.connect() as conn_check:
                result = conn_check.execute(text("SELECT tablename FROM pg_tables WHERE schemaname='public' AND tablename='sales';"))
                if result.fetchone():
                    log("Tabela sales ainda existe após DROP. Abortando CREATE.")
                else:
                    if create_sales:
                        try:
                            log(f"[DEBUG] Executando CREATE TABLE sales:")
                            log(create_sales.group())
                            with engine.connect() as conn_create:
                                conn_create.execute(text(create_sales.group()))
                            log("[DEBUG] CREATE TABLE sales executado.")
                        except Exception as e:
                            log(f"Erro ao executar CREATE TABLE sales isolado: {e}")
            # Remove apenas DROP/CREATE da tabela sales para não executar novamente
            sql_script = re.sub(r"DROP TABLE IF EXISTS sales;?", "", sql_script)
            sql_script = re.sub(r"CREATE TABLE sales[\s\S]+?\)\s*;?", "", sql_script)
            with engine.connect() as conn:
                for stmt in sql_script.split(';'):
                    if stmt.strip():
                        try:
                            conn.execute(text(stmt))
                        except Exception as e:
                            log(f"Erro ao executar comando SQL: {e}\nComando: {stmt.strip()[:100]}")
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
    Se a tabela existir mas estiver com a coluna 'date', corrige o schema antes de qualquer operação.
    Executa o script completo de reset (DROP TABLE + CREATE TABLE + INSERT).
    """
    auto_reset = os.getenv("DB_AUTO_RESET", "true").lower() == "true"
    if not auto_reset:
        log("Reset automático desabilitado.")
        return
    try:
        with engine.connect() as conn:
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
                sql_script = process_sql_script(sql_script)
                # Executa DROP/CREATE isolado
                import re
                drop_sales = re.search(r"DROP TABLE IF EXISTS sales", sql_script)
                create_sales = re.search(r"CREATE TABLE\s+sales\s*\([\s\S]+?\);", sql_script, re.IGNORECASE)
                # Executa DROP isolado com retry e isolamento AUTOCOMMIT
                import time
                max_attempts = 3
                for attempt in range(max_attempts):
                    try:
                        # Usa AUTOCOMMIT para evitar erro de configuração
                        with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn_drop:
                            conn_drop.execute(text("DROP TABLE IF EXISTS sales"))
                        break
                    except Exception as e:
                        log(f"Erro ao executar DROP TABLE sales isolado (tentativa {attempt+1}): {e}")
                        if "database is locked" in str(e) and attempt < max_attempts - 1:
                            log("Se o erro persistir, feche todos os processos/editores que estejam usando o arquivo moura.db e tente novamente.")
                            import time
                            time.sleep(2)
                        else:
                            log("Se o erro persistir, feche outros processos/terminais que estejam usando o banco SQLite.")
                            break
                # Verifica se a tabela foi removida
                with engine.connect() as conn_check:
                    result = conn_check.execute(text("SELECT tablename FROM pg_tables WHERE schemaname='public' AND tablename='sales';"))
                    if result.fetchone():
                        log("Tabela sales ainda existe após DROP. Abortando CREATE.")
                    else:
                        # Executa CREATE isolado
                        if create_sales:
                            try:
                                with engine.connect() as conn_create:
                                    conn_create.execute(text(create_sales.group()))
                            except Exception as e:
                                log(f"Erro ao executar CREATE TABLE sales isolado: {e}")
                # Remove apenas DROP/CREATE da tabela sales para não executar novamente
                sql_script = re.sub(r"DROP TABLE IF EXISTS sales;?", "", sql_script)
                sql_script = re.sub(r"CREATE TABLE sales[\s\S]+?\)\s*;?", "", sql_script)
                with engine.connect() as conn:
                    for stmt in sql_script.split(';'):
                        if stmt.strip():
                            try:
                                conn.execute(text(stmt))
                            except Exception as e:
                                log(f"Erro ao executar comando SQL: {e}\nComando: {stmt.strip()[:100]}")
                log("Banco resetado e populado com dados de exemplo.")
            else:
                log("Tabela 'sales' já existe, está correta e populada.")
    except Exception as e:
        log(f"Erro ao resetar banco: {e}")