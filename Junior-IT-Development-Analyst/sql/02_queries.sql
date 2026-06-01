-- Consultas analíticas para o dashboard de produção

-- 1. KPIs Gerais
SELECT
    COUNT(DISTINCT v.id_venda) AS total_vendas,
    SUM(v.valor_total) AS receita_total,
    AVG(v.valor_total) AS ticket_medio,
    SUM(v.quantidade) AS unidades_vendidas,
    COUNT(DISTINCT v.regiao) AS regioes_ativas
FROM vendas.vendas v
WHERE v.data_venda >= CURRENT_DATE - INTERVAL '30 days';

-- 2. Top 5 produtos por receita
SELECT
    p.nome AS produto,
    SUM(v.quantidade) AS total_unidades,
    SUM(v.valor_total) AS receita_total,
    RANK() OVER (ORDER BY SUM(v.valor_total) DESC) AS rank
FROM vendas.vendas v
JOIN producao.produtos p ON v.id_produto = p.id_produto
WHERE v.data_venda >= CURRENT_DATE - INTERVAL '6 months'
GROUP BY p.nome
ORDER BY receita_total DESC
LIMIT 5;

-- 3. Receita por região (com % do total)
SELECT
    v.regiao,
    SUM(v.valor_total) AS receita,
    ROUND(SUM(v.valor_total) * 100.0 / SUM(SUM(v.valor_total)) OVER (), 2) AS pct_receita,
    COUNT(*) AS qtd_vendas
FROM vendas.vendas v
GROUP BY v.regiao
ORDER BY receita DESC;

-- 4. Série temporal de produção (semanal)
SELECT
    DATE_TRUNC('week', op.data_inicio) AS semana,
    COUNT(DISTINCT op.id_ordem) AS total_ordens,
    SUM(op.quantidade_planejada) AS unidades_planejadas,
    SUM(op.quantidade_produzida) AS unidades_produzidas,
    CASE
        WHEN SUM(op.quantidade_planejada) > 0
        THEN ROUND(SUM(op.quantidade_produzida) * 100.0 / SUM(op.quantidade_planejada), 2)
        ELSE 0
    END AS eficiencia_pct
FROM producao.ordens_producao op
WHERE op.data_inicio >= CURRENT_DATE - INTERVAL '3 months'
GROUP BY semana
ORDER BY semana;

-- 5. Eficiência por máquina (manutenção)
SELECT
    m.maquina,
    COUNT(*) AS total_manutencoes,
    AVG(m.duracao_horas) AS media_duracao,
    SUM(m.custo) AS custo_total,
    COUNT(CASE WHEN m.tipo = 'corretiva' THEN 1 END) AS manutencoes_corretivas,
    ROUND(
        COUNT(CASE WHEN m.tipo = 'corretiva' THEN 1 END) * 100.0 / NULLIF(COUNT(*), 0),
        2
    ) AS pct_corretivas
FROM manutencao.manutencoes m
WHERE m.status = 'concluido'
GROUP BY m.maquina
ORDER BY pct_corretivas DESC;

-- 6. Produtos com estoque baixo (menos de 10 ordens no mês)
SELECT
    p.nome,
    COUNT(op.id_ordem) AS ordens_mes,
    COALESCE(SUM(op.quantidade_produzida), 0) AS total_produzido
FROM producao.produtos p
LEFT JOIN producao.ordens_producao op
    ON p.id_produto = op.id_produto
    AND op.data_inicio >= DATE_TRUNC('month', CURRENT_DATE)
WHERE p.ativo = TRUE
GROUP BY p.nome
HAVING COUNT(op.id_ordem) < 10
ORDER BY ordens_mes;

-- 7. Análise de canais de venda
SELECT
    v.canal_venda,
    COUNT(*) AS total_vendas,
    SUM(v.valor_total) AS receita,
    AVG(v.valor_total) AS ticket_medio,
    COUNT(DISTINCT v.regiao) AS regioes_alcancadas
FROM vendas.vendas v
GROUP BY v.canal_venda
ORDER BY receita DESC;

-- 8. Top vendedores do trimestre
SELECT
    v.vendedor,
    COUNT(*) AS vendas_realizadas,
    SUM(v.valor_total) AS receita_gerada,
    ROUND(AVG(v.valor_total), 2) AS ticket_medio,
    RANK() OVER (ORDER BY SUM(v.valor_total) DESC) AS posicao
FROM vendas.vendas v
WHERE v.data_venda >= DATE_TRUNC('quarter', CURRENT_DATE)
GROUP BY v.vendedor
ORDER BY posicao
LIMIT 10;
