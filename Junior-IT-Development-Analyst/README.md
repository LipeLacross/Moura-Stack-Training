# Junior IT Development Analyst — Projeto Portfólio

Este projeto demonstra **todas as competências** da vaga de **Analista de Desenvolvimento TI JR** do **Grupo Moura**. Cada seção abaixo explica **o que é**, **por que a Moura pede**, **como funciona** e **o que foi implementado**.

---

## 📋 Índice completo

| # | Requisito | Explicado no tópico |
|---|-----------|---------------------|
| 1 | Python | [#1](#1-python) |
| 2 | SQL Intermediário | [#2](#2-sql-intermediário) |
| 3 | BPM | [#3](#3-bpm-business-process-management) |
| 4 | Fundamentos de TI | [#4](#4-fundamentos-de-ti) |
| 5 | Power Platform | [#5](#5-power-platform) |
| 6 | Azure Boards | [#6](#6-azure-boards) |
| 7 | Análise de Requisitos | [#7](#7-análise-de-requisitos) |
| 8 | Especificação Técnica | [#8](#8-especificação-técnica) |
| 9 | Metodologias Ágeis | [#9](#9-metodologias-ágeis) |
| 10 | Integração entre Sistemas | [#10](#10-integração-entre-sistemas) |
| 11 | ETL / ELT | [#11](#11-etl-elt) |
| 12 | Dashboards | [#12](#12-dashboards) |
| 13 | ML — Classificação | [#13](#13-machine-learning-classificação) |
| 14 | ML — Regressão | [#14](#14-machine-learning-regressão) |
| 15 | ML — Clusterização | [#15](#15-machine-learning-clusterização) |
| 16 | Feature Engineering | [#16](#16-feature-engineering) |
| 17 | LLMs via API | [#17](#17-llms-via-api) |
| 18 | Prompt Engineering | [#18](#18-prompt-engineering) |
| 19 | IA Generativa | [#19](#19-ia-generativa) |
| 20 | Gestão de Tickets | [#20](#20-gestão-de-tickets-de-suporte) |
| 21 | Treinamento de Usuários | [#21](#21-treinamento-de-usuários) |
| 22 | Inglês Técnico | [#22](#22-inglês-técnico) |
| 23 | .NET / C# | [#23](#23-net-c) |
| 24 | JavaScript | [#24](#24-javascript) |
| 25 | SAP Scripts | [#25](#25-sap-scripts) |
| 26 | FIGMA | [#26](#26-figma) |
| 27 | Bizagi | [#27](#27-bizagi) |

---

### 1. 🐍 Python

**O que a vaga pede:** "Conhecimento em linguagens de programação Python"

**Por que a Moura pede:** Python é a linguagem principal para automação, APIs, análise de dados e ML. Na Moura, scripts Python automatizam processos manuais no SAP, geram relatórios no Power BI e integram sistemas legados.

**Como funciona:**

Python é uma linguagem interpretada (não precisa compilar). O código é executado linha por linha por um interpretador. Sua sintaxe simples permite escrever programas complexos com poucas linhas.

**No dia a dia do Analista TI JR:**
```python
# 1. Automatizar uma tarefa repetitiva
import pandas as pd

df = pd.read_csv("vendas.csv")
resumo = df.groupby("produto")["valor"].sum()
resumo.to_excel("resumo_vendas.xlsx")

# 2. Chamar uma API
import requests
response = requests.post("http://api.moura.com/sync", json={"dados": df.to_dict()})
print(response.json())
```

**Explicação dos termos técnicos usados no projeto:**

| Termo | O que é |
|-------|---------|
| **FastAPI** | Biblioteca Python para criar **APIs REST** (servidores que respondem requisições HTTP) |
| **Pydantic** | Biblioteca que **valida dados** automaticamente (garante que o JSON recebido tem os campos corretos) |
| **Routers** | Forma de organizar os endpoints em arquivos separados (ex: `routers/ml.py` só tem endpoints de ML) |
| **scikit-learn** | Biblioteca de Machine Learning com algoritmos prontos (RandomForest, KMeans, etc.) |
| **pandas** | Biblioteca para **manipular dados** em tabelas (DataFrames). Lê CSV, Excel, SQL, etc. |
| **Streamlit** | Biblioteca que cria **dashboards web** com Python puro (sem HTML/JS) |
| **Plotly** | Biblioteca de **gráficos interativos** (zoom, hover, clicar para filtrar) |
| **Scheduler** | Agendador de tarefas (executa uma função todo dia às 8h, por exemplo) |

**O que foi implementado no projeto:**

| Módulo | Arquivos | O que faz |
|--------|----------|-----------|
| API REST | `src/python/api/` | 9 endpoints com FastAPI, models Pydantic, routers |
| Automação | `src/python/automation/` | Envio de e-mail, processamento de arquivos, scheduler |
| ML | `src/python/ml/` | 3 modelos scikit-learn + feature engineering |
| LLM | `src/python/llm/` | Cliente OpenAI, prompts, geradores de relatório |
| ETL | `src/python/data/` | Pipeline extract-transform-load |
| Dashboard | `src/python/dashboard/` | Streamlit com gráficos Plotly |

---

### 2. 🗄️ SQL Intermediário

**O que a vaga pede:** "SQL Intermediário"

**Por que a Moura pede:** Toda operação da Moura (produção, vendas, estoque) está em bancos PostgreSQL. Você precisa consultar, atualizar e automatizar dados.

**Como funciona:**

SQL é a linguagem para se comunicar com bancos relacionais. "Intermediário" significa que você domina:

| Operação | O que faz | Exemplo |
|----------|-----------|---------|
| `SELECT ... JOIN` | Junta dados de 2+ tabelas | `SELECT v.*, p.nome FROM vendas v JOIN produtos p` |
| `GROUP BY` + `SUM/AVG` | Agrega dados por categoria | `SUM(valor) GROUP BY regiao` |
| `WHERE` com subquery | Filtra com base em outra consulta | `WHERE id IN (SELECT id FROM ...)` |
| `WITH` (CTE) | **Common Table Expression** — cria uma "tabela temporária" que só existe durante a consulta. Útil para organizar queries complexas | `WITH vendas_2024 AS (SELECT * FROM vendas WHERE ano = 2024) SELECT ...` |
| `RANK() OVER` | **Window Function** — calcula ranking sem agrupar os dados (cada linha mantém sua identidade). Diferente de `GROUP BY` que junta linhas | `RANK() OVER (ORDER BY receita DESC)` → 1º, 2º, 3º... |

> **CTE** vs **Subquery**: Ambos fazem coisas parecidas, mas CTE é mais legível. Subquery é aninhada dentro do `WHERE`/`FROM`; CTE é definida antes com `WITH`.

**Stored Procedure — como funciona:**

Uma procedure é um bloco de código SQL salvo no banco que pode ser chamado como uma função. O banco executa no servidor, não no seu computador.

```sql
-- Criar
CREATE PROCEDURE finalizar_ordem(id INT, qtd INT)
LANGUAGE plpgsql AS $$     -- plpgsql = linguagem do PostgreSQL (PL/pgSQL)
BEGIN
    UPDATE ordens_producao SET status = 'concluida', quantidade = qtd WHERE id_ordem = id;
END;
$$;

-- Chamar (igual chamar uma função)
CALL finalizar_ordem(1, 500);
```

**Trigger — como funciona:**

Um trigger "dispara" automaticamente quando algo acontece na tabela (INSERT, UPDATE, DELETE). Executa uma função antes ou depois da operação.

```sql
-- Exemplo: validar quantidade antes de inserir
CREATE TRIGGER trg_valida_qtd
BEFORE INSERT ON ordens_producao   -- Antes de inserir, executa a função
FOR EACH ROW                        -- Para cada linha inserida
EXECUTE FUNCTION valida_quantidade();
```

**View — como funciona:**

Uma **view** é uma "consulta salva". Você usa `SELECT * FROM view` como se fosse uma tabela, mas por baixo executa a query. Útil para não repetir consultas complexas.

```sql
-- Criar view
CREATE VIEW vw_top_produtos AS
SELECT p.nome, SUM(v.valor_total) as receita
FROM vendas v JOIN produtos p ON v.id_produto = p.id_produto
GROUP BY p.nome ORDER BY receita DESC;

-- Usar (mesma sintaxe de tabela)
SELECT * FROM vw_top_produtos WHERE receita > 10000;
```

**O que foi implementado:**

| Arquivo | Objetos | Linhas |
|---------|---------|--------|
| `01_schema.sql` | 4 tabelas, 7 índices | Schema completo |
| `02_queries.sql` | 8 consultas analíticas | KPIs, rankings, tendências |
| `03_procedures.sql` | 4 procedures + 3 tabelas | Automação de processos |
| `04_triggers.sql` | 4 triggers | Validação, auditoria, log |
| `05_analytics.sql` | 5 views analíticas | Performance, saúde, previsão |

---

### 3. 📋 BPM (Business Process Management)

**O que a vaga pede:** "Noção de BPM — Mapear e documentar fluxo de processos"

**BPM NÃO é um app.** BPM é uma **metodologia de gestão** (Business Process Management = Gerenciamento de Processos de Negócio). É a prática de entender, documentar, analisar e melhorar processos.

**BPMN** é a **linguagem/notação** usada para desenhar esses processos. Pense como um "flowchart" universal que qualquer empresa entende.

**Ferramentas que usam BPMN:** Bizagi Modeler (grátis), Azure Logic Apps, Camunda, Visio. Os arquivos `.bpmn` são XML que essas ferramentas abrem.

**Por que a Moura pede:** A Moura precisa documentar e padronizar processos (vendas, produção, suporte). Antes de automatizar com código, você precisa desenhar o fluxo no BPMN.

**Exemplo concreto — processo de vendas em BPMN:**

```
INÍCIO → [Validar Pedido] → DECISÃO: Pedido válido?
  │ SIM                          │ NÃO
  ▼                              ▼
[Consultar Estoque]         [Rejeitar Pedido]
  │                              │
  ▼                              ▼
[Criar Ordem Produção]      FIM (Rejeitado)
  │
  ▼
[Faturar Pedido]
  │
  ▼
FIM (Concluído)
```

Os símbolos BPMN que você precisa saber:
| Símbolo | Nome | O que significa |
|---------|------|----------------|
| ○ | Start Event | Onde o processo começa |
| □ | Task | Uma atividade feita por pessoa ou sistema |
| ◇ | Gateway | Ponto de decisão (ex: "é válido? sim/não") |
| ● | End Event | Onde o processo termina |
| → | Sequence Flow | Seta indicando o fluxo |

**O que foi implementado:**
- `docs/bpmn/processo_vendas.bpmn` — arquivo XML BPMN 2.0 com 2 gateways, 5 tasks
- `docs/bpmn/processo_suporte.bpmn` — fluxo de suporte TI (triagem N1 → N2 → N3)
- Para visualizar: abra no **Bizagi Modeler** (gratuito) ou em qualquer editor BPMN

---

### 4. 🌐 Fundamentos de TI

**O que a vaga pede:** "Fundamentos de TI (Redes, Segurança da Informação, Sistemas Operacionais)"

**O que significam esses termos:**

| Termo | Explicação |
|-------|-----------|
| **Rede** | Conjunto de computadores conectados que trocam dados. A internet é a maior rede |
| **TCP/IP** | Protocolo padrão da internet. Divide os dados em pacotes e garante que cheguem ao destino |
| **HTTP/HTTPS** | Protocolo que seu navegador usa para acessar sites. HTTPS é a versão criptografada |
| **Porta** | "Porta lógica" — número que identifica qual serviço está rodando. Ex: porta 80 = web, 443 = HTTPS, 5432 = PostgreSQL, 8000 = nossa API |
| **localhost** | Endereço `127.0.0.1` — seu próprio computador. Quando você acessa `localhost:8000`, está acessando um servidor rodando na sua máquina |
| **Firewall** | Programa que bloqueia conexões não autorizadas |
| **CORS** | Mecanismo de segurança do navegador que impede sites maliciosos de acessar sua API |
| **.env** | Arquivo que guarda **variáveis de ambiente** (senhas, chaves de API). Nunca é enviado para o GitHub |
| **Docker** | Ferramenta que cria "containers" — ambientes isolados com tudo que o projeto precisa para rodar |

**Como funciona no projeto:**

**Redes:**
```
Seu navegador ──HTTPS──→ Servidor FastAPI (porta 8000) ──TCP──→ PostgreSQL (porta 5432)
    │                                                             │
    │ Conexão via internet ou rede local                          │
    │ (localhost = mesma máquina)                                 │
```

- A API "escuta" na porta 8000. Quando você abre `http://localhost:8000/docs`, o navegador se conecta nessa porta.
- O banco PostgreSQL "escuta" na porta 5432. A API se conecta a ele para buscar/salvar dados.

**Segurança aplicada:**
- **Senhas e chaves** ficam no arquivo `.env` (ex: `DATABASE_URL=postgresql://user:pass@localhost:5432/moura`). Esse arquivo está no `.gitignore` — nunca vai para o GitHub.
- **CORS** configurado: só domínios autorizados podem chamar a API (evita que sites externos usem seus endpoints).
- **Validação de entrada:** toda requisição é validada por modelos Pydantic antes de processar. Se vier um campo inválido, a API devolve erro 422.

**Sistemas Operacionais:**
- O projeto funciona em **Windows**, **Linux** e **macOS**.
- Comandos mudam um pouco: Windows usa `pip` + `python`, Linux/macOS às vezes usam `pip3` + `python3`.
- Se usar **Docker**, o ambiente fica idêntico em qualquer SO.

---

### 5. ⚡ Power Platform

**O que a vaga pede:** "Power Platform (Power Automate, Power BI)"

**Power Platform NÃO é um app único.** É um **conjunto de ferramentas** da Microsoft chamado de "plataforma low-code" (pouco ou nenhum código). Dentro dela existem vários produtos:

**Power Automate** → automatiza tarefas repetitivas
**Power BI** → cria dashboards e relatórios
**Power Apps** → cria aplicativos mobile/desktop
**Power Virtual Agents** → cria chatbots

---

**Power Automate** — O que é?
É um **site/serviço** (https://make.powerautomate.com) onde você cria **fluxos de automação** sem programar. Você usa blocos visuais como LEGO:

```
📌 GATILHO (dispara o fluxo):
   "Quando uma nova linha for inserida na tabela ordens_producao"

   ⬇️

🔧 CONDIÇÃO:
   "Se valor_total > 50.000"
   │
   ├── SIM 📧 "Enviar e-mail para gestor: 'Aprovar ordem #123'"
   │
   └── NÃO ✅ "Atualizar status para 'aprovado automático'"
```

No dia a dia: você usa Power Automate para coisas como "quando chegar e-mail com nota fiscal, baixar o PDF e salvar no SharePoint".

---

**Power BI** — O que é?
É um **app/serviço** (https://app.powerbi.com) para criar **dashboards interativos**. Ele se conecta ao banco de dados (PostgreSQL, SQL Server) e cria gráficos com medidas DAX.

**DAX** é a linguagem de fórmulas do Power BI. Exemplos reais do projeto:

```dax
// Medida: Receita acumulada no ano
Receita YTD = TOTALYTD(SUM(vendas[valor]), calendario[Data])

// Medida: Margem bruta percentual
Margem = DIVIDE([Receita] - [Custo], [Receita])

// Medida: Ticket médio por venda
Ticket Médio = DIVIDE(SUM(vendas[valor]), COUNTROWS(vendas))
```

No dia a dia: você conecta o Power BI ao banco da Moura, cria um dashboard que o gerente acompanha ao vivo no celular.

---

**O que foi implementado:**
- `power-platform/power-automate/` — 2 fluxos documentados (aprovação e notificação)
- `power-platform/power-bi/` — 12 medidas DAX + layout do dashboard (4 abas)
- `power-platform/power-apps/` — App mobile com 5 telas documentadas

---

### 6. 📊 Azure Boards

**O que a vaga pede:** "Azure Boards"

**Azure Boards É um app (web).** É um **site** dentro do Azure DevOps (https://dev.azure.com) que times de TI usam para **organizar tarefas**.

Dentro do Azure Boards, você cria **Work Items** — cartões que representam tarefas:

| Tipo | O que é | Exemplo |
|------|---------|---------|
| Epic | Projeto grande | "Sistema de Automação Moura" |
| Feature | Funcionalidade | "API REST de processos" |
| Story (US) | Necessidade do usuário | "Como analista, quero criar processos via API" |
| Task | Tarefa técnica | "Criar endpoint POST /api/processes" |
| Bug | Erro a corrigir | "Endpoint GET retorna 500 sem autenticação" |

Cada item tem: **prioridade**, **responsável**, **story points** (esforço), **status** (To Do / Doing / Done).

**Hierarquia visual:**

```
📁 Epic: Sistema de Automação         ← Projeto
 └── 📋 Feature: API REST             ← Funcionalidade
      ├── 📝 Story: CRUD Processos (8 pts)   ← O que o usuário quer
      │    ├── 🔧 Task: GET endpoint (2 pts) ← Tarefa técnica
      │    ├── 🔧 Task: POST endpoint (2 pts)
      │    └── 🔧 Task: Testes (2 pts)
      └── 📝 Story: Integração SAP (5 pts)
```

No dia a dia: você abre o Azure Boards, vê o que tem que fazer na sprint, move o cartão de "To Do" para "Doing", e na daily fala "estou fazendo a task X".

**O que foi implementado:**
- `agile/azure-boards/backlog.md` — backlog completo: 5 sprints com 22 itens (epics, stories, tasks)
- `agile/azure-boards/sprint_planning.md` — template de planning com DoD, daily scrum, burndown

---

### 7. 📝 Análise de Requisitos

**O que a vaga pede:** "Desenvolver análise de requisitos"

**Como funciona:** É o processo de descobrir O QUE o sistema precisa fazer. Envolve entrevistar usuários, documentar funcionalidades (RF), restrições (RNF) e regras de negócio (RN).

**O que foi implementado:**

**Requisitos Funcionais (RF):** O sistema DEVE fazer X
- RF01: CRUD de processos
- RF02: Dashboard com KPIs  
- RF03: ML preditivo
- RF04: IA generativa
- RF05: Integração entre sistemas
- RF06: ETL pipeline

**Requisitos Não Funcionais (RNF):** O sistema DEVE SER X
- RNF01: Performance (< 500ms)
- RNF02: Segurança (validação, .env)
- RNF03: Disponibilidade (99.9%)

**Regras de Negócio (RN):** Regras da empresa
- RN01: Quantidade > 0 e ≤ 100.000
- RN02: Manutenção corretiva gera alerta
- RN03: Relatório só com dados consolidados

**Arquivos:** `docs/requisitos/analise_requisitos.md` + `docs/requisitos/historias_usuario.md`

---

### 8. 📐 Especificação Técnica

**O que a vaga pede:** "Especificação técnica"

**Como funciona:** Documento que traduz os requisitos em decisões técnicas: quais tecnologias, arquitetura, endpoints, banco de dados.

**O que foi implementado:** `docs/especificacao_tecnica.md` com arquitetura, stack, endpoints, schema, instruções de execução.

---

### 9. 🏃 Metodologias Ágeis

**O que a vaga pede:** "Metodologias Ágeis"

**Como funciona:** Scrum divide o trabalho em **sprints** (ciclos de 2 semanas). Cada sprint tem:
- **Planning:** time decide o que fazer
- **Daily:** reunião de 15min para alinhamento
- **Review:** mostra o que foi feito
- **Retro:** melhoria contínua

**O que foi implementado:** `agile/scrum-guide.md` com papéis, cerimônias, artefatos e estimativas.

---

### 10. 🔗 Integração entre Sistemas

**O que a vaga pede:** "Analisar e corrigir Integração entre sistemas"

**Como funciona:** Integração conecta dois sistemas para trocarem dados. O padrão mais comum é via **API REST**: um sistema envia uma requisição HTTP, o outro responde com dados JSON.

```
SAP ──POST /sync──→ Middleware ──INSERT──→ PostgreSQL
                     ↓ log
              Tabela log_operacoes
```

**Endpoints implementados:**

```bash
# Sincronizar SAP → Power BI
curl -X POST http://localhost:8000/api/integration/sync \
  -H "Content-Type: application/json" \
  -d '{"source_system":"sap","target_system":"powerbi","payload":{"items":[]}}'

# Resposta:
# {"status":"success","sync_id":"a1b2c3","records_processed":150}
```

**O que foi implementado:**
- `src/python/api/routers/integration.py` — 3 endpoints
- `docs/api_integration.md` — guia com exemplos
- Log de auditoria em `producao.log_operacoes`

---

### 11. 🔄 ETL / ELT

**O que a vaga pede:** "Desenvolver projetos de Dados (ETL e ELT)"

**O que significam esses termos:**

| Termo | Explicação |
|-------|-----------|
| **ETL** | **Extract, Transform, Load** — processo de pegar dados crus, limpar, e salvar em formato pronto para análise |
| **ELT** | Mesma ideia mas a Transformação acontece **depois** de carregar no banco. Mais usado em Big Data |
| **pandas** | Biblioteca Python que trabalha com dados em tabela (DataFrame). Lê CSV, Excel, SQL, JSON |
| **DataFrame** | Tabela na memória do Python. Linhas e colunas, igual Excel |
| **Parquet** | Formato de arquivo **mais rápido e compacto** que CSV. Guarda dados binários (não texto). PySpark e Power BI leem direto |
| **Camada Gold** | Última camada de dados — dados prontos para consumo (relatórios, dashboards, ML) |
| **Camada Silver** | Dados limpos e padronizados, mas ainda não agregados |
| **Camada Bronze** | Dados crus como chegaram (CSV original, log bruto) |
| **SQLAlchemy** | Biblioteca que conecta Python a bancos SQL (PostgreSQL, MySQL, SQLite). Permite escrever SQL direto ou usar ORM |

**Como funciona:**

**ETL = Extract + Transform + Load**

```
📂 data/sample/        🐍 pandas              📁 gold/
   vendas.csv    ──→   DataFrame      ──→     vendas.parquet
   estoque.csv          (limpeza)              (pronto para análise)
                        ↓
                    fill NA (preencher vazios)
                    rename columns
                    converter tipos
                    remover duplicatas
```

**Cada etapa no código:**

```python
# EXTRACT: lê arquivos CSV de um diretório
import pandas as pd
df = pd.concat([pd.read_csv(f) for f in csv_files])  # DataFrame na memória

# TRANSFORM: limpa dados
df = df.fillna(0)                                     # preenche valores vazios com 0
df.columns = [c.strip().lower() for c in df.columns]   # padroniza nomes das colunas
df["data"] = pd.to_datetime(df["data"])                # converte texto para data

# LOAD: salva como Parquet (camada Gold)
df.to_parquet("gold/vendas.parquet")                   # 10x mais rápido que CSV
```

**O que foi implementado:**
- `src/python/data/etl_pipeline.py` — pipeline completo com 6 operações (drop, fill, rename, filter, cast, add)
- `src/python/data/validators.py` — 7 validadores (missing, outliers, tipos, email, range, etc.)
- `src/python/data/database.py` — conexão SQLAlchemy para PostgreSQL

---

### 12. 📊 Dashboards

**O que a vaga pede:** "Desenvolver dashboards"

**Como funciona:** Um dashboard coleta dados de várias fontes e apresenta em gráficos e KPIs. O Streamlit recarrega a página automaticamente quando o código muda.

**Streamlit Dashboard — tela real do projeto:**
```
┌─────────────────────────────────────────────────────┐
│ R$ 2.4M   12.500 unid    89.2%     4 produtos       │
│ ┌─────────────────────────────────────────────────┐ │
│ │           Gráfico Plotly interativo             │ │
│ │  ▁▂▃▅▇▆▅▆▇▆▅▃▂▁                                 │ │
│ └─────────────────────────────────────────────────┘ │
│ Tab1: Série Temporal | Tab2: Distribuição           │
│ Tab3: ML Predictions | Tab4: Relatório IA           │
└─────────────────────────────────────────────────────┘
```

**O que foi implementado:**
- `src/python/dashboard/app.py` — Streamlit com Plotly
- `power-platform/power-bi/medidas_dax.md` — 12 medidas DAX

---

### 13. 🤖 Machine Learning — Classificação

**O que a vaga pede:** "Modelos de machine learning (classificação)"

**O que significam esses termos:**

| Termo | Explicação |
|-------|-----------|
| **Classificação** | Tipo de ML que prevê uma **categoria** (ex: "falha sim ou não?", "cliente A, B ou C?") |
| **RandomForest** | Algoritmo que cria **várias árvores de decisão** e combina o resultado. Cada árvore "vota". Mais votos = resposta final. É como perguntar para 100 especialistas e fazer média |
| **Feature** | Coluna de entrada do modelo (ex: temperatura, vibração, pressão). O modelo aprende padrões nelas |
| **Target** | Coluna que queremos prever (ex: 0 = máquina normal, 1 = máquina vai falhar) |
| **Feature Importance** | O modelo diz qual feature **mais impacta** a decisão. Ex: "vibração é 2x mais importante que temperatura" |

**Como funciona o RandomForest:**

```
🌳 Árvore 1: "temperatura > 80? sim → risco, não → normal"
🌳 Árvore 2: "vibração > 0.5? sim → risco, não → normal"
🌳 Árvore 3: "pressão > 100 E horas > 500? sim → risco, não → normal"
... (100 árvores no total)

VOTAÇÃO:
  72 árvores votaram "risco" (1)
  28 árvores votaram "normal" (0)
  → RESULTADO: Risco (probabilidade 72%)
```

**Métricas de avaliação:**

| Métrica | Pergunta que responde | Fórmula mental |
|---------|----------------------|----------------|
| **Accuracy** | De todas as previsões, quantas acertamos? | `acertos / total` |
| **Precision** | Quando o modelo disse "risco", quantas vezes acertou? | `riscos verdadeiros / (riscos verdadeiros + falsos alarmes)` |
| **Recall** | Dos riscos reais, quantos o modelo detectou? | `riscos verdadeiros / (riscos verdadeiros + riscos perdidos)` |
| **F1-score** | Média entre precision e recall (equilíbrio) | `2 * (precision * recall) / (precision + recall)` |

**O que foi implementado:** `src/python/ml/classifier.py` — RandomForest com 100 árvores, 5 features, 4 métricas de avaliação

---

### 14. 📈 Machine Learning — Regressão

**O que a vaga pede:** "Modelos de machine learning (regressão)"

**Como funciona:** Em vez de classes, a regressão prevê um **número contínuo**. O RandomForestRegressor calcula a média das previsões de todas as árvores.

```
Features: [temp_ambiente, umidade, velocidade, qualidade]
    ↓
RandomForestRegressor
    ↓
Eficiência prevista: 87.3%
```

**Métricas:**
- **RMSE:** erro médio (em unidades da variável)
- **MAE:** erro absoluto médio
- **R²:** quanto da variância os dados explicam (0 a 1)

**O que foi implementado:** `src/python/ml/regressor.py`

---

### 15. 🔬 Machine Learning — Clusterização

**O que a vaga pede:** "Modelos de machine learning (clustering)"

**O que significam esses termos:**

| Termo | Explicação |
|-------|-----------|
| **Clusterização** | Tipo de ML que **agrupa dados similares** sem supervisão (não precisa de respostas certas para treinar) |
| **KMeans** | Algoritmo que divide os dados em K grupos. Cada grupo tem um centro (centroide). Cada ponto pertence ao centroide mais próximo |
| **Centroide** | Ponto central de um cluster. É a média de todos os pontos daquele grupo |
| **K** | Número de grupos que você quer encontrar (no projeto: K=3) |
| **Silhouette Score** | Mede quão bem separados estão os clusters. Vai de -1 a 1. Quanto mais próximo de 1, melhor |

**Como funciona o KMeans:**

```
PASSO 1: Escolher K=3 (3 grupos)
PASSO 2: Sortear 3 pontos aleatórios como centros iniciais
PASSO 3: Para cada máquina, calcular qual centro está mais perto
PASSO 4: Mover cada centro para o meio do seu grupo
PASSO 5: Repetir passos 3-4 até os centros pararem de mudar

RESULTADO:
   Cluster 0 → máquinas com consumo baixo, operação normal → "Eficientes"
   Cluster 1 → máquinas com alto consumo e temperatura → "Estresse"
   Cluster 2 → máquinas com poucas horas de operação → "Ociosas"

Nova máquina: [consumo=30, horas=500, temp=85]
  → Calcular distância para cada centroide
  → Centro mais próximo: Cluster 1 (Estresse)
  → Similaridade: 0.87 (87% similar ao grupo)
```

**Diferença entre Classificação e Clusterização:**

| Classificação (item 13) | Clusterização (item 15) |
|------------------------|------------------------|
| Precisa de dados rotulados para treinar | Não precisa de rótulos |
| Você diz as categorias antes | O algoritmo descobre os grupos |
| Ex: "isso é SPAM ou não?" | Ex: "quais clientes são similares?" |

**O que foi implementado:** `src/python/ml/clustering.py` — KMeans com K=3, silhouette score, predição para novos pontos

---

### 16. 🧮 Feature Engineering

**O que a vaga pede:** "Realizar feature engineering"

**O que é:** Criar **novas colunas** a partir das existentes para dar mais "informação" para o modelo de ML. Um modelo com boas features aprende melhor.

**O que significam esses termos:**

| Técnica | Explicação | Exemplo |
|---------|-----------|---------|
| **Time features** | Extrair informações de uma data | `2024-01-15` → ano, mês, dia, dia_da_semana, fim_de_semana, trimestre |
| **Lag (defasagem)** | Usar o valor de ontem para prever hoje | `lag_1` = produção de ontem. `lag_7` = produção de 7 dias atrás |
| **Rolling window** | Média móvel de um período | `rolling_mean_7` = média dos últimos 7 dias. `rolling_std_7` = desvio padrão |
| **Aggregate features** | Estatísticas por grupo | Para cada máquina: média de produção, desvio padrão, mínimo, máximo |
| **One-hot encoding** | Transformar categoria em colunas 0/1 | Turno: `manha=[1,0,0]`, `tarde=[0,1,0]`, `noite=[0,0,1]` |
| **Label encoding** | Transformar categoria em números 1,2,3 | Turno: `manha=1`, `tarde=2`, `noite=3` |
| **Interaction** | Multiplicar duas features | `temperatura * vibracao` — pode revelar padrões que cada feature sozinha não mostra |

**Exemplo prático:**

```
Coluna original: data = "2024-01-15 08:30:00"

Feature Engineering aplicado:
  → ano = 2024
  → mes = 1
  → dia = 15
  → dia_semana = 2 (0=domingo, 1=segunda, 2=terça...)
  → hora = 8
  → fim_semana = 0 (não é sábado nem domingo)
  → trimestre = 1 (jan-mar)

Coluna original: producao = [100, 95, 102, 98, 105, 97, 101, 99, ...]
  → producao_lag_1 = 100 (o valor de ontem)
  → producao_lag_7 = 101 (o valor de 7 dias atrás)
  → producao_rolling_mean_7 = 99.7 (média dos últimos 7 dias)
  → producao_rolling_std_7 = 3.2 (variação dos últimos 7 dias)
```

**O que foi implementado:** `src/python/ml/feature_engineering.py` — 6 métodos de criação de features (time, lag, rolling, aggregate, encoding, interaction)

---

### 17. 🌐 LLMs via API

**O que a vaga pede:** "Integrar APIs de LLMs"

**Como funciona:** LLMs (Large Language Models) como GPT-4o recebem texto (prompt) e geram texto novo. A comunicação é via API REST:

```
[Seu código] ──HTTP POST──→ [OpenAI API]
  Prompt: "Gere um relatório..."     |
  ←── Resposta: "## Relatório..." ───┘
```

```python
from openai import OpenAI
client = OpenAI(api_key="sk-...")
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Explique BPMN"}]
)
print(response.choices[0].message.content)
```

**Explicação dos termos técnicos:**

| Termo | O que é |
|-------|---------|
| **LLM** | Large Language Model — modelo de IA treinado com bilhões de textos para gerar e compreender linguagem natural |
| **OpenAI API** | Serviço pago (pay-per-use) que permite enviar prompts para modelos GPT via requisições HTTP |
| **GPT** | Generative Pre-trained Transformer — arquitetura de modelo criada pela OpenAI |
| **Token** | Unidade de texto que o LLM processa (1 token ≈ 0.75 palavra em inglês). O custo é por token |
| **Chat Completion** | Formato de API onde você envia uma lista de mensagens (system, user, assistant) e recebe uma resposta |
| **Temperature** | Parâmetro que controla a criatividade: 0 = sempre a mesma resposta, 1 = mais criativo/aleatório |
| **Model** | Versão específica do GPT (ex: gpt-4o-mini é mais rápido e barato que gpt-4o) |

**O que foi implementado:** `src/python/llm/client.py` — cliente configurável (OpenAI / Azure OpenAI).

---

### 18. 🎯 Prompt Engineering

**O que a vaga pede:** "Prompt engineering básico"

**Como funciona:** A qualidade da resposta da IA depende da qualidade do prompt. Regras básicas:

| Regra | Ruim | Bom |
|-------|------|-----|
| Seja específico | "Gere um relatório" | "Gere um relatório técnico com: resumo, análise de KPIs e 3 recomendações" |
| Dê contexto | "Analise isso" | "Analise o sentimento do feedback: 'O sistema é lento'" |
| Defina formato | "Responda" | "Responda em JSON com campos: sentimento, confianca" |

**O que foi implementado:** `src/python/llm/prompts.py` — 3 templates com melhor prática de prompting.

---

### 19. 🧠 IA Generativa

**O que a vaga pede:** "Implementar soluções básicas com IA generativa"

**Como funciona:** IA generativa Cria conteúdo novo (texto, código). Difere da IA discriminativa que apenas classifica ou prevê.

**Pipeline de geração de relatório:**
```
Dashboard KPIs → Resumo JSON → LLM Prompt → Relatório em texto
                     ↓                        ↓
             {"receita": 2400000,       "## Resumo Executivo
              "eficiencia": 89.2,        No período analisado..."
              "taxa_falhas": 3.5}
```

**O que foi implementado:** `src/python/llm/generators.py` — 3 geradores com fallback offline.

---

### 20. 🎫 Gestão de Tickets de Suporte

**O que a vaga pede:** "Gestão de tickets de suporte e monitoramento"

**Fluxo de suporte implementado (BPMN):**

```
[Ticket Aberto] → [Triagem]
    ↓ N1 (básico)          ↓ N2 (analista)
[Suporte resolve]    [Analista investiga]
    ↓                     ↓
    └──◇ Resolveu?──┘
        Sim → [Ticket Fechado] + [Log]
        Não → [Escalar N3]
```

**Monitoramento:** Endpoint `GET /health` retorna status da API e da conexão com banco.

---

### 21. 👨‍🏫 Treinamento de Usuários

**O que a vaga pede:** "Treinamento de usuários sobre utilização dos sistemas"

**O que foi implementado:** `docs/treinamento_usuario.md` — guia completo com módulos, comandos, erros comuns e FAQ.

---

### 22. 🇬🇧 Inglês Técnico

**O que a vaga pede:** "Inglês Técnico (leitura)"

**Aplicado no projeto:** Código usa nomes em inglês (variáveis, funções, classes). Documentação alterna PT-BR (explicações) com EN (termos técnicos: endpoint, payload, feature, pipeline).

---

### 23. 💻 .NET / C#

**O que a vaga pede:** "Conhecimento em .NET, C#"

**Como funciona:** ASP.NET Core cria APIs no padrão **Controller → Service**. O Controller recebe a requisição HTTP, chama o Service que tem a lógica, e retorna a resposta.

```
HTTP GET /api/process → ProcessController.GetAll()
                          → ProcessService.GetAll()
                              ← List<ProcessModel>
                          ← JSON
```

**Explicação dos termos técnicos:**

| Termo | O que é |
|-------|---------|
| **.NET** | Plataforma de desenvolvimento da Microsoft para criar aplicativos Windows, Web, APIs |
| **ASP.NET Core** | Framework web do .NET para criar APIs e sites. Roda em Windows, Linux e macOS |
| **C#** | Linguagem de programação principal do .NET. Compilada, tipada, orientada a objetos |
| **Controller** | Classe que recebe requisições HTTP e define endpoints. Ex: `ProcessController.Get()` |
| **Service** | Classe com a lógica de negócio. O Controller chama o Service, que processa e retorna dados |
| **Swagger / OpenAPI** | Interface web que documenta e testa os endpoints da API automaticamente. Acessível em `/swagger` |
| **DTO** | Data Transfer Object — objeto simples que carrega dados entre camadas (Controller → Service) |
| **Dependency Injection** | Padrão onde o framework cria e injeta automaticamente as dependências (ex: Service dentro do Controller) |

**O que foi implementado:** `src/dotnet/ProcessAutomation.Api/` — 6 endpoints, Swagger.

---

### 24. 🌐 JavaScript

**O que a vaga pede:** "Conhecimento em JavaScript"

**Como funciona:** O frontend faz requisições `fetch()` para a API e renderiza os resultados no DOM.

```javascript
// api-client.js encapsula todas as chamadas
const api = new MouraApiClient('http://localhost:8000');
const processos = await api.getProcesses();
// renderiza na tabela HTML
```

**Explicação dos termos técnicos:**

| Termo | O que é |
|-------|---------|
| **DOM** | Document Object Model — representação em árvore do HTML que o JavaScript manipula para alterar a página |
| **Chart.js** | Biblioteca JavaScript para criar gráficos interativos (barras, pizza, linhas) em canvas HTML |
| **Fetch API** | Função nativa do JavaScript para fazer requisições HTTP (GET, POST, PUT, DELETE) |
| **async/await** | Sintaxe moderna para lidar com operações assíncronas (API calls, arquivos) sem travar a página |
| **Promise** | Objeto que representa uma operação que ainda não terminou. `await` "espera" a Promise resolver |
| **Arrow Function** | Sintaxe encurtada de função: `(x) => x * 2` ao invés de `function(x) { return x * 2 }` |

**O que foi implementado:** `src/javascript/` — Dashboard com Chart.js, CRUD, integração.

---

### 25. 📜 SAP Scripts

**O que a vaga pede:** "Conhecimento SAP Scripts"

**Como funciona:** SAP GUI permite automação via VBScript. O script controla a interface do SAP como se fosse um usuário (preenche campos, clica botões).

```vbscript
' Exemplo: entrar transação, preencher campo, executar
Session.findById("wnd[0]/tbar[0]/okcd").text = "/nVA03"
Session.findById("wnd[0]/usr/ctxtVBAK-VBELN").text = "10000001"
Session.findById("wnd[0]").sendVKey 0
```

**Explicação dos termos técnicos:**

| Termo | O que é |
|-------|---------|
| **SAP GUI** | Programa desktop que se conecta ao servidor SAP e mostra a interface do sistema (campos, botões, telas) |
| **VBScript** | Linguagem de script da Microsoft (Visual Basic Scripting) que automatiza programas Windows |
| **Transaction Code** | Código que abre uma tela específica no SAP. Ex: `/nVA03` = exibir pedido de venda |
| **Session** | Objeto que representa a janela atual do SAP GUI. Toda automação começa com `Session.findById(...)` |
| **BAPI** | Business API — função oficial do SAP para integração entre sistemas (mais estável que automação GUI) |
| **RFC** | Remote Function Call — protocolo de comunicação do SAP para chamar funções remotamente |
| **sendVKey** | Comando que simula pressionar uma tecla no SAP (Enter, F8 = executar, F3 = voltar) |

**O que foi implementado:** `sap/sap_scripts.md` — 3 scripts + integração com Python.

---

### 26. 🎨 FIGMA

**O que a vaga pede:** "Conhecimento FIGMA"

**O que foi implementado:** `figma/` — Design system (cores, tipografia, componentes) + wireframes de 5 telas descritos em markdown.

---

### 27. 📊 Bizagi

**O que a vaga pede:** "Conhecimento Bizagi"

**O que foi implementado:** `docs/bpmn/*.bpmn` — arquivos BPMN 2.0 que podem ser abertos no Bizagi Modeler (grátis) para edição visual.

---

## 🚀 Execução completa

```bash
# 1. API (http://localhost:8000/docs)
uvicorn src.python.api.main:app --reload --port 8000

# 2. Dashboard (http://localhost:8501)
streamlit run src/python/dashboard/app.py

# 3. Frontend JS (http://localhost:3000)
cd src/javascript && npx http-server src -p 3000

# 4. .NET API (http://localhost:5000/swagger)
cd src/dotnet && dotnet run --project ProcessAutomation.Api

# 5. Testes
pytest tests/ -v
```

---

## 🏗️ Estrutura resumida

```
src/python/      → API + automação + ML + LLM + ETL + dashboard
src/dotnet/      → API C#
src/javascript/  → Frontend
sql/             → 5 arquivos SQL (schema → analytics)
docs/            → Requisitos, BPMN, especificação, treinamento
power-platform/  → Automate, BI, Apps
agile/           → Scrum, Azure Boards
figma/           → Design system, wireframes
sap/             → Scripts SAP
tests/           → Testes Python + SQL
```

---

> Projeto portfólio para **Analista de Desenvolvimento TI JR — Grupo Moura**.
