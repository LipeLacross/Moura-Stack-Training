# Análise de Requisitos - Sistema de Automação de Processos Moura TI

## 1. Visão Geral

**Projeto:** Sistema Integrado de Automação, Monitoramento e Análise de Processos  
**Cliente:** Grupo Moura - TI Corporativa  
**Versão:** 1.0  
**Data:** Maio/2026

## 2. Objetivos

Automatizar processos de negócio, integrar sistemas legados (SAP, bancos SQL), gerar dashboards analíticos com ML e IA generativa, e centralizar o monitoramento de produção.

## 3. Requisitos Funcionais

### RF01 - Automação de Processos
- **Descrição:** Permitir criação, edição e exclusão de fluxos de automação via API REST.
- **Prioridade:** Alta
- **Critérios de Aceite:**
  - CRUD completo de processos
  - Agendamento de tarefas (diário, semanal, por intervalo)
  - Execução de scripts Python automatizados

### RF02 - Dashboard de KPIs
- **Descrição:** Exibir indicadores de produção, vendas e eficiência em tempo real.
- **Prioridade:** Alta
- **Critérios de Aceite:**
  - Gráficos interativos (Chart.js / Plotly)
  - Filtros por período, produto e região
  - Exportação para CSV e Excel

### RF03 - Machine Learning
- **Descrição:** Modelos de classificação, regressão e clustering para análise preditiva.
- **Prioridade:** Média
- **Critérios de Aceite:**
  - Classificação de falhas em máquinas
  - Regressão para previsão de eficiência
  - Clustering de padrões de produção
  - Feature engineering automatizada

### RF04 - Integração com LLM / IA Generativa
- **Descrição:** Geração de relatórios técnicos e documentação via IA.
- **Prioridade:** Média
- **Critérios de Aceite:**
  - Geração de relatório executivo a partir de KPIs
  - Documentação automática de processos
  - Análise de sentimento de feedbacks

### RF05 - Integração entre Sistemas
- **Descrição:** Sincronizar dados entre SAP, Power BI, Azure Boards e bancos SQL.
- **Prioridade:** Alta
- **Critérios de Aceite:**
  - Webhook para sincronização
  - Log completo de operações
  - Suporte a múltiplos protocolos (REST, ODBC)

### RF06 - ETL e Camada de Dados
- **Descrição:** Pipeline de extração, transformação e carga de dados.
- **Prioridade:** Alta
- **Critérios de Aceite:**
  - Suporte a CSV, JSON, Parquet, Excel
  - Pipeline configurável (drop columns, fill NA, rename)
  - Geração de dados de amostra para testes

## 4. Requisitos Não Funcionais

### RNF01 - Performance
- Resposta da API em < 500ms (p95)
- Modelos ML carregam em < 2s
- Dashboard renderiza em < 3s

### RNF02 - Segurança
- Autenticação via API Key (a ser implementada)
- Validação de entrada em todos os endpoints
- Logs de auditoria no banco

### RNF03 - Disponibilidade
- API disponível 99.9% (exceto manutenção programada)
- Banco PostgreSQL com replicação

### RNF04 - Manutenibilidade
- Código modular e testado (>80% cobertura)
- Documentação técnica e de usuário
- Padrão REST consistente

## 5. Stakeholders

| Papel | Nome | Envolvimento |
|-------|------|--------------|
| PO | Gerente de TI | Prioriza backlog |
| Dev | Analista TI JR | Desenvolve e testa |
| Usuário | Analista de Produção | Usa dashboards |
| Usuário | Supervisor de Manutenção | Usa ML predictions |

## 6. Diagrama de Casos de Uso

```
+--------------------+       +-------------------------+
| Analista de Produção|------>| Dashboard de KPIs      |
+--------------------+       +-------------------------+
                                     |
+--------------------+       +-------------------------+
| Supervisor         |------>| ML - Previsão de Falhas |
+--------------------+       +-------------------------+
                                     |
+--------------------+       +-------------------------+
| Equipe de TI       |------>| API de Automação       |
+--------------------+       +-------------------------+
                                     |
+--------------------+       +-------------------------+
| Gestor             |------>| Relatório Gerado por IA |
+--------------------+       +-------------------------+
```

## 7. Regras de Negócio

1. **RN01:** Toda ordem de produção deve ter quantidade > 0 e <= 100.000
2. **RN02:** Manutenção corretiva gera alerta automático para equipe
3. **RN03:** Relatório executivo só pode ser gerado com dados consolidados do mês
4. **RN04:** Sincronização entre sistemas deve manter log de auditoria
5. **RN05:** Modelos ML devem ser retreinados mensalmente
