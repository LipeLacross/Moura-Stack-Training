import os
from sqlalchemy import text
from app.backend.db import engine


def init_db_if_needed():
    """
    Inicializa o banco executando o SQL de 01_init.sql se a tabela 'sales' não existir.
    Pode ser desabilitado via DB_AUTO_INIT=false.
    """
    auto_init = os.getenv("DB_AUTO_INIT", "true").lower() == "true"
    if not auto_init:
        print("[DB INIT] Inicialização automática desabilitada.")
        return
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' AND table_name = 'sales'
                )
            """))
            exists = result.scalar()
            if exists:
                print("[DB INIT] Tabela 'sales' já existe. Nenhuma ação necessária.")
                return
            print("[DB INIT] Tabela 'sales' não existe. Executando script de inicialização...")
            sql_path = os.path.join(os.path.dirname(__file__), '../../sql/01_init.sql')
            with open(sql_path, encoding="utf-8") as f:
                sql = f.read()
            # Executa múltiplos comandos
            for cmd in sql.split(';'):
                cmd = cmd.strip()
                if cmd:
                    conn.execute(text(cmd))
            print("[DB INIT] Script de inicialização executado com sucesso.")
    except Exception as e:
        print(f"[DB INIT] Erro ao inicializar o banco: {e}")
