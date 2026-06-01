# Histórias de Usuário

## Epic 1: Automação de Processos

### US01 - Criar Fluxo de Automação
> **Como** Analista de TI  
> **Quero** criar um novo fluxo de automação via API  
> **Para** reduzir tarefas manuais repetitivas

**Critérios de Aceite:**
- Informar nome, descrição e passos do fluxo
- Receber ID único do fluxo criado
- Validação de campos obrigatórios

### US02 - Agendar Tarefa Automática
> **Como** Analista de TI  
> **Quero** agendar uma tarefa para execução diária às 8h  
> **Para** que relatórios sejam gerados automaticamente

**Critérios de Aceite:**
- Escolher frequência (diária, semanal, por minutos)
- Associar uma função Python ao agendamento
- Visualizar tarefas agendadas

## Epic 2: Dashboard e KPIs

### US03 - Visualizar Dashboard de Produção
> **Como** Analista de Produção  
> **Quero** ver KPIs de produção em tempo real  
> **Para** tomar decisões rápidas sobre a operação

**Critérios de Aceite:**
- Cards com receita, volume, eficiência
- Gráfico de série temporal
- Filtro por período

### US04 - Exportar Relatório
> **Como** Analista de Produção  
> **Quero** exportar dados para CSV ou Excel  
> **Para** compartilhar com a gestão

## Epic 3: Machine Learning

### US05 - Classificar Risco de Falha
> **Como** Supervisor de Manutenção  
> **Quero** classificar máquinas quanto ao risco de falha  
> **Para** priorizar manutenção preventiva

**Critérios de Aceite:**
- Informar features da máquina
- Receber classificação (0 = normal, 1 = risco)
- Ver probabilidade e importância das features

### US06 - Prever Eficiência
> **Como** Supervisor de Produção  
> **Quero** prever a eficiência da produção com base em parâmetros  
> **Para** ajustar processos antecipadamente

### US07 - Agrupar Padrões de Produção
> **Como** Analista de Dados  
> **Quero** agrupar máquinas por padrões operacionais  
> **Para** identificar clusters de desempenho

## Epic 4: IA Generativa

### US08 - Gerar Relatório Executivo
> **Como** Gestor de TI  
> **Quero** gerar um relatório executivo automaticamente  
> **Para** apresentar resultados na reunião de diretoria

**Critérios de Aceite:**
- Informar período e métricas
- Receber relatório em markdown
- Incluir análises e recomendações

## Epic 5: Integração entre Sistemas

### US09 - Sincronizar Dados SAP -> Power BI
> **Como** Analista de TI  
> **Quero** sincronizar dados do SAP para o Power BI  
> **Para** manter dashboards atualizados automaticamente

**Critérios de Aceite:**
- Especificar sistemas origem e destino
- Enviar payload com dados
- Receber ID de sincronização e status

### US10 - Gerenciar Tickets de Suporte
> **Como** Analista de TI  
> **Quero** gerenciar tickets de suporte dos sistemas  
> **Para** garantir a estabilidade das operações

## Backlog Técnico

- BT01: Implementar autenticação JWT
- BT02: Configurar CI/CD com GitHub Actions
- BT03: Criar container Docker da aplicação
- BT04: Implementar testes de carga na API
- BT05: Configurar monitoramento com Prometheus
