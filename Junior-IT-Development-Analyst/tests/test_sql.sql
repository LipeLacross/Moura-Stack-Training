-- Testes para validação das queries SQL
-- Execute em um banco PostgreSQL de teste

BEGIN;

-- 1. Verificar se o schema foi criado
SELECT schema_name FROM information_schema.schemata
WHERE schema_name IN ('producao', 'vendas', 'manutencao', 'analytics');

-- 2. Verificar tabelas
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'producao';

-- 3. Testar procedure de finalizar ordem
CALL producao.finalizar_ordem(1, 50, 'Teste automatizado');

-- 4. Verificar trigger de updated_at
UPDATE producao.ordens_producao SET observacao = 'teste' WHERE id_ordem = 1;
SELECT updated_at > created_at AS trigger_funcionou
FROM producao.ordens_producao WHERE id_ordem = 1;

-- 5. Testar validação de quantidade (deve falhar)
DO $$
BEGIN
    BEGIN
        UPDATE producao.ordens_producao SET quantidade_planejada = 0 WHERE id_ordem = 1;
        RAISE EXCEPTION 'TESTE FALHOU: Trigger não bloqueou quantidade zero';
    EXCEPTION
        WHEN OTHERS THEN
            RAISE NOTICE 'Trigger funcionou: %', SQLERRM;
    END;
END;
$$;

-- 6. Verificar views analytics
SELECT * FROM analytics.vw_performance_mensal LIMIT 5;
SELECT * FROM analytics.vw_ranking_produtos LIMIT 5;
SELECT * FROM analytics.vw_saude_maquinas LIMIT 5;

ROLLBACK;
