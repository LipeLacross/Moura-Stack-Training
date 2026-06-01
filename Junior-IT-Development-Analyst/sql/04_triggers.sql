-- Triggers para automação de regras de negócio

-- 1. Trigger: atualizar estoque após venda
CREATE OR REPLACE FUNCTION vendas.atualizar_estoque()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_estoque_atual INT;
BEGIN
    SELECT COALESCE(SUM(op.quantidade_produzida - op.quantidade_planejada), 0)
    INTO v_estoque_atual
    FROM producao.ordens_producao op
    WHERE op.id_produto = NEW.id_produto AND op.status = 'concluida';

    INSERT INTO producao.log_operacoes (tabela, operacao, registro_id, detalhes)
    VALUES (
        'vendas',
        'INSERT',
        NEW.id_venda,
        format('Venda de %s unidades do produto %s. Estoque aproximado: %s',
               NEW.quantidade, NEW.id_produto, v_estoque_atual - NEW.quantidade)
    );

    RETURN NEW;
END;
$$;

CREATE OR REPLACE TRIGGER trg_venda_atualiza_estoque
    AFTER INSERT ON vendas.vendas
    FOR EACH ROW
    EXECUTE FUNCTION vendas.atualizar_estoque();

-- 2. Trigger: atualizar updated_at automaticamente
CREATE OR REPLACE FUNCTION producao.set_updated_at()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;

CREATE OR REPLACE TRIGGER trg_ordens_updated_at
    BEFORE UPDATE ON producao.ordens_producao
    FOR EACH ROW
    EXECUTE FUNCTION producao.set_updated_at();

-- 3. Trigger: validar quantidade mínima em ordens de produção
CREATE OR REPLACE FUNCTION producao.validar_quantidade_minima()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF NEW.quantidade_planejada < 1 THEN
        RAISE EXCEPTION 'Quantidade planejada deve ser maior que zero';
    END IF;
    IF NEW.quantidade_planejada > 100000 THEN
        RAISE EXCEPTION 'Quantidade planejada excede o limite de 100.000 unidades';
    END if;
    RETURN NEW;
END;
$$;

CREATE OR REPLACE TRIGGER trg_ordens_valida_quantidade
    BEFORE INSERT OR UPDATE ON producao.ordens_producao
    FOR EACH ROW
    EXECUTE FUNCTION producao.validar_quantidade_minima();

-- 4. Trigger: notificar quando manutenção corretiva for registrada
CREATE OR REPLACE FUNCTION manutencao.notificar_manutencao_corretiva()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF NEW.tipo = 'corretiva' THEN
        INSERT INTO producao.log_operacoes (tabela, operacao, registro_id, detalhes)
        VALUES (
            'manutencao',
            'INSERT',
            NEW.id_manutencao,
            format('MANUTENCAO CORRETIVA: Maquina %s - Tecnico: %s - Custo: R$ %s',
                   NEW.maquina, NEW.tecnico_responsavel, NEW.custo)
        );

        -- Atualizar status de ordens associadas à máquina
        UPDATE producao.ordens_producao op
        SET status = CASE WHEN op.status = 'em_andamento' THEN 'pendente' ELSE op.status END
        FROM producao.produtos p
        WHERE op.id_produto = p.id_produto
          AND p.nome LIKE '%' || NEW.maquina || '%'
          AND op.status NOT IN ('concluida', 'cancelada');
    END IF;
    RETURN NEW;
END;
$$;

CREATE OR REPLACE TRIGGER trg_notifica_manutencao_corretiva
    AFTER INSERT ON manutencao.manutencoes
    FOR EACH ROW
    WHEN (NEW.tipo = 'corretiva')
    EXECUTE FUNCTION manutencao.notificar_manutencao_corretiva();
