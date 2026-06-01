-- Stored Procedures para automação de processos

-- 1. Procedure para registrar produção concluída
CREATE OR REPLACE PROCEDURE producao.finalizar_ordem(
    p_id_ordem INT,
    p_quantidade_real INT,
    p_observacao TEXT DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE producao.ordens_producao
    SET
        quantidade_produzida = p_quantidade_real,
        data_fim = CURRENT_TIMESTAMP,
        status = 'concluida',
        observacao = COALESCE(p_observacao, observacao),
        updated_at = CURRENT_TIMESTAMP
    WHERE id_ordem = p_id_ordem;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Ordem de produção % não encontrada', p_id_ordem;
    END IF;

    -- Registrar log
    INSERT INTO producao.log_operacoes (tabela, operacao, registro_id, detalhes)
    VALUES ('ordens_producao', 'UPDATE', p_id_ordem,
            format('Ordem finalizada: %s unidades produzidas', p_quantidade_real));
END;
$$;

-- 2. Procedure para consolidar vendas diárias
CREATE OR REPLACE PROCEDURE vendas.consolidar_vendas_dia(
    p_data DATE DEFAULT CURRENT_DATE
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO vendas.resumo_diario (data, total_vendas, receita_total, quantidade_total)
    SELECT
        DATE(v.data_venda),
        COUNT(*),
        SUM(v.valor_total),
        SUM(v.quantidade)
    FROM vendas.vendas v
    WHERE DATE(v.data_venda) = p_data
    GROUP BY DATE(v.data_venda)
    ON CONFLICT (data) DO UPDATE
    SET
        total_vendas = EXCLUDED.total_vendas,
        receita_total = EXCLUDED.receita_total,
        quantidade_total = EXCLUDED.quantidade_total;

    RAISE NOTICE 'Vendas consolidadas para %', p_data;
END;
$$;

-- 3. Procedure para agendar manutenção preventiva
CREATE OR REPLACE PROCEDURE manutencao.agendar_preventiva(
    p_maquina VARCHAR(20),
    p_data_sugerida DATE
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_ultima_manutencao DATE;
    v_dias_desde_ultima INT;
BEGIN
    -- Verificar última manutenção
    SELECT MAX(data_realizada) INTO v_ultima_manutencao
    FROM manutencao.manutencoes
    WHERE maquina = p_maquina AND status = 'concluido';

    v_dias_desde_ultima := COALESCE(p_data_sugerida - v_ultima_manutencao, 999);

    IF v_dias_desde_ultima >= 30 OR v_ultima_manutencao IS NULL THEN
        INSERT INTO manutencao.manutencoes (
            maquina, tipo, data_agendada, status
        ) VALUES (
            p_maquina, 'preventiva', p_data_sugerida, 'pendente'
        );
        RAISE NOTICE 'Manutenção preventiva agendada para % em %', p_maquina, p_data_sugerida;
    ELSE
        RAISE NOTICE 'Máquina % já foi mantida há % dias', p_maquina, v_dias_desde_ultima;
    END IF;
END;
$$;

-- 4. Procedure de backup de tabelas antigas
CREATE OR REPLACE PROCEDURE producao.arquivar_dados_antigos(
    p_meses_retroativos INT DEFAULT 12
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_data_corte DATE;
BEGIN
    v_data_corte := CURRENT_DATE - (p_meses_retroativos || ' months')::INTERVAL;

    -- Arquivar ordens de produção antigas
    INSERT INTO producao.ordens_producao_arquivo
    SELECT * FROM producao.ordens_producao
    WHERE data_inicio < v_data_corte AND status = 'concluida';

    DELETE FROM producao.ordens_producao
    WHERE data_inicio < v_data_corte AND status = 'concluida';

    RAISE NOTICE 'Dados arquivados até %', v_data_corte;
END;
$$;

-- Tabela auxiliar para resumo diário
CREATE TABLE IF NOT EXISTS vendas.resumo_diario (
    data DATE PRIMARY KEY,
    total_vendas INT DEFAULT 0,
    receita_total DECIMAL(12,2) DEFAULT 0,
    quantidade_total INT DEFAULT 0,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de log de operações
CREATE TABLE IF NOT EXISTS producao.log_operacoes (
    id_log SERIAL PRIMARY KEY,
    tabela VARCHAR(50),
    operacao VARCHAR(20),
    registro_id INT,
    detalhes TEXT,
    usuario VARCHAR(100) DEFAULT CURRENT_USER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de arquivo para ordens antigas
CREATE TABLE IF NOT EXISTS producao.ordens_producao_arquivo (
    LIKE producao.ordens_producao INCLUDING ALL,
    arquivado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
