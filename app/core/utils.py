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


def init_db_if_needed():
    """
    Inicializa o banco executando o SQL de 01_init.sql se a tabela 'sales' não existir.
    Pode ser desabilitado via DB_AUTO_INIT=false.
    """
    auto_init = os.getenv("DB_AUTO_INIT", "true").lower() == "true"
    if not auto_init:
        log("Inicialização automática desabilitada.")
        return
    try:
        if table_exists():
            log("Tabela 'sales' já existe. Nenhuma ação necessária.")
            return
        log("Tabela 'sales' não existe. Executando script de inicialização...")
        sql_path = os.path.join(os.path.dirname(__file__), '../../sql/01_init.sql')
        if not os.path.exists(sql_path):
            log(f"Arquivo SQL não encontrado: {sql_path}")
            return
        with open(sql_path, encoding="utf-8") as f:
            sql = f.read()
        with engine.connect() as conn:
            try:
                conn.exec_driver_sql(sql)
                log("Script de inicialização executado com sucesso.")
            except Exception as e:
                log(f"Erro ao executar script SQL: {e}")
        # Verificação pós-inicialização
        if table_exists():
            log("Tabela 'sales' criada com sucesso.")
        else:
            log("Falha ao criar tabela 'sales'. Verifique o script SQL.")
    except Exception as e:
        log(f"Erro ao inicializar o banco: {e}")
