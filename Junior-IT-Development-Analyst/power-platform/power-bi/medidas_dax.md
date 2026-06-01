# Medidas DAX - Dashboard Power BI

## Medidas Base

### Receita Total
```dax
Receita Total = SUM(vendas[valor_total])
```

### Quantidade Total
```dax
Quantidade Total = SUM(vendas[quantidade])
```

### Ticket Médio
```dax
Ticket Médio = DIVIDE([Receita Total], COUNTROWS(vendas))
```

### Custo Total
```dax
Custo Total = SUMX(vendas, vendas[quantidade] * RELATED(produtos[preco_custo]))
```

### Margem Bruta
```dax
Margem Bruta = DIVIDE([Receita Total] - [Custo Total], [Receita Total])
```

## Medidas Temporais

### Receita YTD
```dax
Receita YTD = TOTALYTD([Receita Total], dim_calendario[Data])
```

### Receita Mês Anterior
```dax
Receita Mês Anterior = CALCULATE(
    [Receita Total],
    PREVIOUSMONTH(dim_calendario[Data])
)
```

### Variação Mensal (%)
```dax
Var Mensal % = DIVIDE(
    [Receita Total] - [Receita Mês Anterior],
    [Receita Mês Anterior]
)
```

## Medidas de Performance

### Eficiência Média
```dax
Eficiência Média = AVERAGE(producao[eficiencia])
```

### Taxa de Conclusão
```dax
Taxa Conclusão = DIVIDE(
    COUNTROWS(FILTER(ordens_producao, ordens_producao[status] = "concluida")),
    COUNTROWS(ordens_producao)
)
```

### Custo Médio por Manutenção
```dax
Custo Médio Manutenção = AVERAGE(manutencoes[custo])
```

## Medidas de ML

### Risco Médio de Falha
```dax
Risco Médio = AVERAGE(ml_previsoes[probabilidade_falha])
```

### Previsão de Eficiência
```dax
Eficiência Prevista = AVERAGE(ml_previsoes[eficiencia_prevista])
```

## Tabela dim_calendario
```dax
dim_calendario = CALENDAR(
    DATE(2024, 1, 1),
    DATE(2026, 12, 31)
)
```
