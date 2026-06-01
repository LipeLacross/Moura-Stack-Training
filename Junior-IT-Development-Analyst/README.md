# Junior IT Development Analyst - Projeto Portfólio

Projeto-portfólio que demonstra **todas as competências** exigidas na vaga de **Analista de Desenvolvimento TI JR** do **Grupo Moura**. Cada tecnologia, ferramenta e conceito pedido no job description foi implementado neste projeto.

---

## 📋 Índice com Mapeamento Completo da Vaga

| # | Requisito da Vaga | Onde está no Projeto | Status |
|---|-------------------|---------------------|--------|
| 1 | **Python** | `src/python/` - automação, API, ML, ETL | ✅ |
| 2 | **SQL Intermediário** | `sql/` - schema, queries, procedures, triggers, views | ✅ |
| 3 | **BPM (Business Process Management)** | `docs/bpmn/` - fluxos BPMN 2.0 | ✅ |
| 4 | **Fundamentos de TI (Redes, Segurança, SO)** | `docs/especificacao_tecnica.md` - arquitetura, protocolos | ✅ |
| 5 | **Power Platform** | `power-platform/` - Power Automate, Power BI (DAX), Power Apps | ✅ |
| 6 | **Azure Boards** | `agile/azure-boards/` - backlog, sprints | ✅ |
| 7 | **Análise de Requisitos** | `docs/requisitos/` - análise funcional, histórias de usuário | ✅ |
| 8 | **Especificação Técnica** | `docs/especificacao_tecnica.md` | ✅ |
| 9 | **Metodologias Ágeis** | `agile/` - Scrum guide, daily, planning | ✅ |
| 10 | **Integração entre Sistemas** | `src/python/api/routers/integration.py` + `docs/api_integration.md` | ✅ |
| 11 | **ETL / ELT** | `src/python/data/etl_pipeline.py` | ✅ |
| 12 | **Dashboards** | `src/python/dashboard/app.py` (Streamlit) + `power-platform/power-bi/` | ✅ |
| 13 | **Machine Learning (classificação)** | `src/python/ml/classifier.py` - RandomForest | ✅ |
| 14 | **Machine Learning (regressão)** | `src/python/ml/regressor.py` - RandomForest | ✅ |
| 15 | **Machine Learning (clustering)** | `src/python/ml/clustering.py` - KMeans | ✅ |
| 16 | **Feature Engineering** | `src/python/ml/feature_engineering.py` | ✅ |
| 17 | **LLMs via API** | `src/python/llm/client.py` - OpenAI | ✅ |
| 18 | **Prompt Engineering** | `src/python/llm/prompts.py` - templates | ✅ |
| 19 | **IA Generativa** | `src/python/llm/generators.py` - relatórios | ✅ |
| 20 | **Gestão de Tickets** | `src/python/api/routers/` + `docs/bpmn/processo_suporte.bpmn` | ✅ |
| 21 | **Treinamento de Usuários** | `docs/treinamento_usuario.md` | ✅ |
| 22 | **Inglês Técnico** | Código e docs em português + README com termos técnicos | ✅ |

### Diferenciais

| # | Diferencial | Onde está | Status |
|---|-------------|-----------|--------|
| 23 | **.NET / C#** | `src/dotnet/` - API REST completa | ✅ |
| 24 | **JavaScript** | `src/javascript/` - Frontend com Chart.js | ✅ |
| 25 | **SAP Scripts** | `sap/sap_scripts.md` - VBScript + Python | ✅ |
| 26 | **Figma** | `figma/` - Design system + wireframes | ✅ |
| 27 | **Inglês Técnico (leitura)** | Documentação, variáveis e termos em inglês | ✅ |

---

## 🚀 Como Executar

```bash
# 1. Clonar
git clone <url>
cd Junior-IT-Development-Analyst

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Configurar ambiente
cp .env.example .env

# 4. API REST (FastAPI)
uvicorn src.python.api.main:app --reload --port 8000
# Docs: http://localhost:8000/docs

# 5. Dashboard (Streamlit)
streamlit run src/python/dashboard/app.py
# Acessar: http://localhost:8501

# 6. Frontend JavaScript
cd src/javascript
npx http-server src -p 3000
# Acessar: http://localhost:3000

# 7. .NET API
cd src/dotnet
dotnet run --project ProcessAutomation.Api
# Acessar: http://localhost:5000/swagger
```

---

## 🏗️ Estrutura do Projeto

```
Junior-IT-Development-Analyst/
│
├── src/
│   ├── python/                    # 🐍 Python (requisito #1)
│   │   ├── api/                   # REST API (FastAPI)
│   │   ├── automation/            # Automação de tarefas
│   │   ├── ml/                    # Machine Learning
│   │   ├── llm/                   # IA Generativa / LLM
│   │   ├── data/                  # ETL / Banco de Dados
│   │   └── dashboard/             # Streamlit Dashboard
│   │
│   ├── dotnet/                    # 💻 .NET / C# (diferencial #23)
│   │   └── ProcessAutomation.Api/ # API REST em C#
│   │
│   └── javascript/                # 🌐 JavaScript (diferencial #24)
│       └── src/                   # Frontend Chart.js
│
├── sql/                           # 🗄️ SQL (#2)
│   ├── 01_schema.sql              # Schema do banco
│   ├── 02_queries.sql             # Consultas analíticas
│   ├── 03_procedures.sql          # Stored procedures
│   ├── 04_triggers.sql            # Triggers
│   └── 05_analytics.sql           # Views analíticas
│
├── docs/                          # 📝 Documentação
│   ├── requisitos/                # Análise de requisitos (#7)
│   ├── bpmn/                      # BPMN 2.0 (#3)
│   ├── especificacao_tecnica.md   # Especificação técnica (#8)
│   ├── treinamento_usuario.md     # Treinamento (#21)
│   └── api_integration.md         # Integração (#10)
│
├── power-platform/                # ⚡ Power Platform (#5)
│   ├── power-automate/            # Fluxos de automação
│   ├── power-bi/                  # Medidas DAX
│   └── power-apps/                # App mobile
│
├── agile/                         # 🏃 Metodologias Ágeis (#9)
│   ├── azure-boards/              # Azure Boards (#6)
│   └── scrum-guide.md             # Guia Scrum
│
├── figma/                         # 🎨 FIGMA (#26)
│   ├── design-system.md           # Design system
│   └── wireframes.md              # Wireframes
│
├── sap/                           # 📜 SAP Scripts (#25)
│   └── sap_scripts.md             # Automação SAP
│
├── ml/
│   └── models/                    # Modelos treinados
│
├── data/
│   └── sample/                    # Dados de exemplo
│
├── tests/                         # ✅ Testes
│   ├── test_automation.py
│   ├── test_ml.py
│   ├── test_api.py
│   └── test_sql.sql
│
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🐍 Módulo 1: Python

### 1.1 API REST (FastAPI) - `src/python/api/`

Endpoints disponíveis:

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/health` | Health check |
| GET/POST | `/api/processes/` | CRUD de processos |
| POST | `/api/ml/predict` | Predição (classifier/regressor/cluster) |
| POST | `/api/ml/train` | Treinar modelos |
| POST | `/api/llm/generate` | Gerar texto com IA |
| POST | `/api/llm/analyze-sentiment` | Análise de sentimento |
| POST | `/api/llm/generate-report` | Relatório executivo |
| POST | `/api/integration/sync` | Sincronizar sistemas |
| GET | `/api/integration/systems` | Listar sistemas |

### 1.2 Automação - `src/python/automation/`

- `email_reports.py` → Envio automático de relatórios por e-mail
- `file_processor.py` → Leitura/escrita de CSV, Excel, JSON, Parquet
- `scheduler.py` → Agendamento de tarefas (diário, semanal, por intervalo)

### 1.3 Machine Learning - `src/python/ml/`

| Modelo | Arquivo | Algoritmo | Uso |
|--------|---------|-----------|-----|
| Classificação | `classifier.py` | RandomForest | Prever falha em máquina |
| Regressão | `regressor.py` | RandomForest | Prever eficiência |
| Clusterização | `clustering.py` | KMeans | Agrupar padrões |
| Feature Engineering | `feature_engineering.py` | - | Criar features |
| Pipeline | `train_pipeline.py` | - | Treinar todos |

### 1.4 LLM / IA Generativa - `src/python/llm/`

- `client.py` → Cliente OpenAI / Azure OpenAI
- `prompts.py` → Templates de prompt engineering
- `generators.py` → Geradores de relatório, documentação, treinamento

### 1.5 ETL - `src/python/data/`

- `etl_pipeline.py` → Pipeline Extract → Transform → Load
- `database.py` → Conexão PostgreSQL com SQLAlchemy
- `validators.py` → Validação de dados (missing, outliers, tipos)

### 1.6 Dashboard - `src/python/dashboard/`

- `app.py` → Streamlit com KPIs, gráficos Plotly, ML predictions, relatório IA

---

## 🗄️ Módulo 2: SQL

### Schema (`sql/01_schema.sql`)
- `producao.produtos` - Catálogo de produtos
- `producao.ordens_producao` - Ordens de produção
- `vendas.vendas` - Vendas
- `manutencao.manutencoes` - Manutenção de máquinas
- Índices para performance

### Queries Analíticas (`sql/02_queries.sql`)
- KPIs gerais, top produtos, receita por região, série temporal
- Eficiência por máquina, análise de canais, top vendedores

### Stored Procedures (`sql/03_procedures.sql`)
- `finalizar_ordem()` - Concluir ordem de produção
- `consolidar_vendas_dia()` - Consolidar vendas diárias
- `agendar_preventiva()` - Agenda manutenção preventiva
- `arquivar_dados_antigos()` - Arquivar dados históricos

### Triggers (`sql/04_triggers.sql`)
- `trg_venda_atualiza_estoque` - Atualiza estoque após venda
- `trg_ordens_updated_at` - Atualiza timestamp automaticamente
- `trg_ordens_valida_quantidade` - Valida quantidade mínima/máxima
- `trg_notifica_manutencao_corretiva` - Alerta em manutenção corretiva

### Views Analíticas (`sql/05_analytics.sql`)
- `vw_performance_mensal` - Performance mensal de produção
- `vw_ranking_produtos` - Ranking de produtos por receita
- `vw_saude_maquinas` - Saúde das máquinas
- `vw_funil_vendas` - Funil por canal
- `vw_previsao_demanda` - Previsão (média móvel 3 meses)

---

## 📋 Módulo 3: BPM (Business Process Management)

Processos modelados em **BPMN 2.0** (`docs/bpmn/`):

- **Processo de Vendas** → `processo_vendas.bpmn`
  - Início: Pedido Recebido → Validar → Gateway → Consultar Estoque → Criar Ordem → Faturar → Fim
- **Processo de Suporte TI** → `processo_suporte.bpmn`
  - Início: Ticket Aberto → Triagem → Gateway N1/N2 → Gateway Resolvido? → Escalar N3 → Fim

---

## ⚡ Módulo 4: Power Platform

### Power Automate
- `fluxo_aprovacao.md` → Fluxo de aprovação de ordens > R$ 50.000
- `fluxo_notificacao.md` → Notificação de manutenção corretiva no Teams

### Power BI
- `medidas_dax.md` → Medidas DAX (Receita YTD, Margem, Eficiência, etc.)
- `dashboard_producao.md` → Layout do dashboard (4 abas)

### Power Apps
- `app_monitoramento.md` → App mobile com 5 telas + fórmulas PowerFX

---

## 🏃 Módulo 5: Metodologias Ágeis + Azure Boards

- **Scrum Guide** → Papéis (PO, SM, Dev Team), cerimônias, artefatos
- **Azure Boards Backlog** → 5 sprints, 22 itens, história de usuário, tasks
- **Sprint Planning** → Template, DoD, daily scrum, burndown chart
- **Estimativas** → Planning Poker com Fibonacci

---

## 💻 Módulo 6: .NET / C#

API REST em .NET 8 (`src/dotnet/ProcessAutomation.Api/`):

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/process` | Listar processos |
| GET | `/api/process/{id}` | Obter processo |
| POST | `/api/process` | Criar processo |
| PATCH | `/api/process/{id}/status` | Atualizar status |
| DELETE | `/api/process/{id}` | Excluir processo |
| GET | `/api/process/dashboard` | Dashboard de métricas |

---

## 🌐 Módulo 7: JavaScript

Frontend com Chart.js (`src/javascript/`):

- Dashboard com KPIs e gráfico doughnut
- CRUD de processos
- Integração entre sistemas (formulário)
- Cliente API encapsulado (`api-client.js`)

---

## 🎨 Módulo 8: FIGMA

Documentação de design (`figma/`):

- **Design System**: cores, tipografia, componentes (cards, botões, inputs)
- **Wireframes**: 5 telas (Login, Dashboard, Processos, Integração, Relatório IA)

---

## 📜 Módulo 9: SAP Scripts

Automação SAP via VBScript (`sap/sap_scripts.md`):

- Extrair relatório de vendas → CSV
- Criar ordem de produção
- Consultar status de pedido
- Integração com Python via subprocess

---

## ✅ Testes

```bash
# Testes Python
pytest tests/ -v --cov=src.python

# Testes SQL (requer PostgreSQL)
psql -f tests/test_sql.sql
```

---

## 📊 O que cada tecnologia resolve no contexto da Moura

| Tecnologia | Problema que resolve |
|------------|---------------------|
| **Python + Automação** | Tarefas manuais repetitivas → scripts automáticos |
| **SQL + Procedures** | Consultas lentas → dados otimizados com índices |
| **BPMN** | Processos confusos → documentação clara e padronizada |
| **Power Platform** | Falta de integração → automação low-code |
| **Azure Boards** | Desorganização → gestão ágil de projetos |
| **API REST** | Sistemas isolados → integração via webhooks |
| **ETL** | Dados crus → dados prontos para análise |
| **ML** | Reatividade → predição e proatividade |
| **LLM / IA** | Relatórios manuais → geração automática |
| **SAP Scripts** | Tarefas manuais no SAP → automação |

---

## 📌 Resumo para Estudo (Checklist por Área)

### 🐍 Python
- [ ] FastAPI (REST, Pydantic, routers)
- [ ] Automação (smtplib, schedule, pandas)
- [ ] ML (scikit-learn: Classifier, Regressor, KMeans)
- [ ] LLM (OpenAI API, prompt templates)

### 🗄️ SQL
- [ ] CREATE TABLE com constraints
- [ ] SELECT com JOIN, GROUP BY, window functions
- [ ] Stored Procedures (CRUD, consolidação)
- [ ] Triggers (validação, auditoria)
- [ ] Views analíticas

### 📋 BPM
- [ ] BPMN 2.0 (start event, task, gateway, end event)
- [ ] Modelagem de processos
- [ ] Documentação de fluxos

### ⚡ Power Platform
- [ ] Power Automate (triggers, conditions, approvals)
- [ ] Power BI (DAX measures, DirectQuery)
- [ ] Power Apps (telas, galerias, fórmulas)

### 🏃 Agile
- [ ] Scrum (papéis, cerimônias, artefatos)
- [ ] Azure Boards (backlog, sprints, work items)
- [ ] Planning Poker (estimativas)

### 💻 .NET / C#
- [ ] ASP.NET Core Web API
- [ ] Controllers, Models, Services
- [ ] Swagger documentation

### 🌐 JavaScript
- [ ] Fetch API (async/await)
- [ ] Chart.js (gráficos)
- [ ] DOM manipulation

---

> Projeto criado como portfólio para demonstrar competências alinhadas à vaga de **Analista de Desenvolvimento TI JR** do **Grupo Moura**.
