# Power BI - Dashboard de Produção

## Aba 1: Visão Geral
- Card: Receita Total (YTD)
- Card: Unidades Produzidas
- Card: Eficiência Média
- Gráfico: Receita × Mês (linha)
- Gráfico: Top 5 Produtos (barra)

## Aba 2: Detalhamento
- Tabela: Vendas por Região
- Mapa: Distribuição Geográfica
- Gráfico: Canal de Vendas (pizza)
- Filtro: Período (data slicer)

## Aba 3: Manutenção
- Card: Manutenções Corretivas
- Gráfico: Custo × Máquina
- Tabela: Últimas Manutenções
- Indicador: Saúde das Máquinas

## Aba 4: ML Insights
- Gráfico: Importância das Features
- KPI: Previsão de Eficiência
- Tabela: Predições por Máquina

## Configuração de Fonte
- **Tipo:** PostgreSQL
- **Servidor:** localhost
- **Database:** moura_ti
- **Modo:** DirectQuery (para dados em tempo real) ou Import (para melhor performance)
