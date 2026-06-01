-- Views analíticas para dashboards e relatórios

-- 1. View: Performance mensal de produção
CREATE OR REPLACE VIEW analytics.vw_performance_mensal AS
SELECT
    DATE_TRUNC('month', op.data_inicio) AS mes,
    COUNT(DISTINCT op.id_ordem) AS total_ordens,
    SUM(op.quantidade_planejada) AS unidades_planejadas,
    SUM(op.quantidade_produzida) AS unidades_produzidas,
    CASE
        WHEN SUM(op.quantidade_planejada) > 0
        THEN ROUND(SUM(op.quantidade_produzida) * 100.0 / SUM(op.quantidade_planejada), 2)
        ELSE 0
    END AS eficiencia_pct,
    AVG(CASE WHEN op.data_fim IS NOT NULL
             THEN EXTRACT(EPOCH FROM (op.data_fim - op.data_inicio)) / 3600
         END) AS horas_media_producao
FROM producao.ordens_producao op
GROUP BY DATE_TRUNC('month', op.data_inicio)
ORDER BY mes DESC;

-- 2. View: Ranking de produtos
CREATE OR REPLACE VIEW analytics.vw_ranking_produtos AS
SELECT
    p.nome AS produto,
    p.categoria,
    COUNT(DISTINCT v.id_venda) AS total_vendas,
    SUM(v.quantidade) AS unidades_vendidas,
    SUM(v.valor_total) AS receita_gerada,
    ROUND(AVG(v.valor_total), 2) AS ticket_medio,
    COUNT(DISTINCT v.regiao) AS regioes_presentes,
    DENSE_RANK() OVER (ORDER BY SUM(v.valor_total) DESC) AS rank_receita
FROM vendas.vendas v
JOIN producao.produtos p ON v.id_produto = p.id_produto
WHERE v.data_venda >= CURRENT_DATE - INTERVAL '1 year'
GROUP BY p.nome, p.categoria;

-- 3. View: Saúde das máquinas
CREATE OR REPLACE VIEW analytics.vw_saude_maquinas AS
SELECT
    m.maquina,
    COUNT(*) FILTER (WHERE m.tipo = 'corretiva') AS manut_corretivas,
    COUNT(*) FILTER (WHERE m.tipo = 'preventiva') AS manut_preventivas,
    COUNT(*) FILTER (WHERE m.tipo = 'preditiva') AS manut_preditivas,
    ROUND(
        COUNT(*) FILTER (WHERE m.tipo = 'corretiva') * 100.0 / NULLIF(COUNT(*), 0), 2
    ) AS indice_falha_pct,
    SUM(m.custo) AS custo_total_manutencao,
    AVG(m.duracao_horas) AS tempo_medio_parada,
    CASE
        WHEN COUNT(*) FILTER (WHERE m.tipo = 'corretiva') = 0 THEN 'Excelente'
        WHEN COUNT(*) FILTER (WHERE m.tipo = 'corretiva') <= 2 THEN 'Bom'
        WHEN COUNT(*) FILTER (WHERE m.tipo = 'corretiva') <= 5 THEN 'Atenção'
        ELSE 'Crítico'
    END AS classificacao_saude,
    MAX(m.data_realizada) AS ultima_manutencao
FROM manutencao.manutencoes m
WHERE m.status = 'concluido'
GROUP BY m.maquina;

-- 4. View: Funil de vendas por canal
CREATE OR REPLACE VIEW analytics.vw_funil_vendas AS
SELECT
    v.canal_venda,
    COUNT(*) AS leads_contato,
    SUM(v.quantidade) AS propostas_enviadas,
    SUM(v.valor_total) AS negocios_fechados,
    ROUND(AVG(v.valor_total), 2) AS ticket_medio,
    COUNT(DISTINCT v.regiao) AS abrangencia_geografica,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2
    ) AS taxa_conversao_canal
FROM vendas.vendas v
GROUP BY v.canal_venda
ORDER BY negocios_fechados DESC;

-- 5. View: Previsão de demanda (média móvel 3 meses)
CREATE OR REPLACE VIEW analytics.vw_previsao_demanda AS
WITH vendas_mensais AS (
    SELECT
        p.id_produto,
        p.nome AS produto,
        DATE_TRUNC('month', v.data_venda) AS mes,
        SUM(v.quantidade) AS total_vendido
    FROM vendas.vendas v
    JOIN producao.produtos p ON v.id_produto = p.id_produto
    GROUP BY p.id_produto, p.nome, DATE_TRUNC('month', v.data_venda)
)
SELECT
    produto,
    mes,
    total_vendido,
    ROUND(AVG(total_vendido) OVER (
        PARTITION BY id_produto
        ORDER BY mes
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) AS media_movel_3meses,
    CASE
        WHEN total_vendido > AVG(total_vendido) OVER (
            PARTITION BY id_produto ORDER BY mes ROWS BETWEEN 2 PRECEDING AND 1 PRECEDING
        ) * 1.2 THEN 'Crescente'
        WHEN total_vendido < AVG(total_vendido) OVER (
            PARTITION BY id_produto ORDER BY mes ROWS BETWEEN 2 PRECEDING AND 1 PRECEDING
        ) * 0.8 THEN 'Decrescente'
        ELSE 'Estável'
    END AS tendencia
FROM vendas_mensais;

-- Schema para views analíticas
CREATE SCHEMA IF NOT EXISTS analytics;
