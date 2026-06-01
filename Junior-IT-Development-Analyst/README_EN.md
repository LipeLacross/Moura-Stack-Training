# Junior IT Development Analyst — Portfolio Project

This project demonstrates **all technical competencies** required for the **Junior IT Development Analyst** position at **Grupo Moura**. Each section explains **what it is**, **why Moura requires it**, **how it works**, and **what was implemented**.

> ⚠️ The original job posting is closed, but this serves as a **complete study guide** for future opportunities.

---

## 📋 Complete Index

| # | Requirement | Covered in Topic |
|---|-------------|------------------|
| 1 | Python | [#1](#1-python) |
| 2 | Intermediate SQL | [#2](#2-intermediate-sql) |
| 3 | BPM | [#3](#3-bpm-business-process-management) |
| 4 | IT Fundamentals | [#4](#4-it-fundamentals) |
| 5 | Power Platform | [#5](#5-power-platform) |
| 6 | Azure Boards | [#6](#6-azure-boards) |
| 7 | Requirements Analysis | [#7](#7-requirements-analysis) |
| 8 | Technical Specification | [#8](#8-technical-specification) |
| 9 | Agile Methodologies | [#9](#9-agile-methodologies) |
| 10 | System Integration | [#10](#10-system-integration) |
| 11 | ETL / ELT | [#11](#11-etl-elt) |
| 12 | Dashboards | [#12](#12-dashboards) |
| 13 | ML — Classification | [#13](#13-machine-learning-classification) |
| 14 | ML — Regression | [#14](#14-machine-learning-regression) |
| 15 | ML — Clustering | [#15](#15-machine-learning-clustering) |
| 16 | Feature Engineering | [#16](#16-feature-engineering) |
| 17 | LLMs via API | [#17](#17-llms-via-api) |
| 18 | Prompt Engineering | [#18](#18-prompt-engineering) |
| 19 | Generative AI | [#19](#19-generative-ai) |
| 20 | Ticket Management | [#20](#20-ticket-management) |
| 21 | User Training | [#21](#21-user-training) |
| 22 | Technical English | [#22](#22-technical-english) |
| 23 | .NET / C# | [#23](#23-net-c) |
| 24 | JavaScript | [#24](#24-javascript) |
| 25 | SAP Scripts | [#25](#25-sap-scripts) |
| 26 | FIGMA | [#26](#26-figma) |
| 27 | Bizagi | [#27](#27-bizagi) |

---

### 1. 🐍 Python

**What the job requires:** "Knowledge of Python programming language"

**Why Moura requires it:** Python is the main language for automation, APIs, data analysis, and ML. At Moura, Python scripts automate manual SAP processes, generate Power BI reports, and integrate legacy systems.

**How it works:**

Python is an interpreted language (no compilation needed). Code runs line by line through an interpreter. Its simple syntax lets you write complex programs in few lines.

**On a Junior Analyst's daily routine:**
```python
# 1. Automate repetitive tasks
import pandas as pd
df = pd.read_csv("sales.csv")
summary = df.groupby("product")["value"].sum()
summary.to_excel("sales_summary.xlsx")

# 2. Call an API
import requests
resp = requests.post("http://api.moura.com/sync", json={"data": df.to_dict()})
```

**Explanation of technical terms:**

| Term | What it is |
|------|-----------|
| **FastAPI** | Python library for creating **REST APIs** (servers that respond to HTTP requests) |
| **Pydantic** | Library that **validates data** automatically (ensures received JSON has correct fields) |
| **Routers** | Way to organize endpoints in separate files (e.g., `routers/ml.py` only has ML endpoints) |
| **scikit-learn** | Machine Learning library with ready-to-use algorithms (RandomForest, KMeans, etc.) |
| **pandas** | Library for **data manipulation** in tables (DataFrames). Reads CSV, Excel, SQL, etc. |
| **Streamlit** | Library that creates **web dashboards** with pure Python (no HTML/JS) |
| **Plotly** | Library for **interactive charts** (zoom, hover, click to filter) |
| **Scheduler** | Task scheduler (runs a function daily at 8am, for example) |

**What was implemented:**

| Module | Files | Purpose |
|--------|-------|---------|
| REST API | `src/python/api/` | 9 endpoints with FastAPI, Pydantic models |
| Automation | `src/python/automation/` | Email, file processing, task scheduling |
| ML | `src/python/ml/` | 3 scikit-learn models + feature engineering |
| LLM | `src/python/llm/` | OpenAI client, prompts, report generators |
| ETL | `src/python/data/` | Extract-transform-load pipeline |
| Dashboard | `src/python/dashboard/` | Streamlit with Plotly charts |

---

### 2. 🗄️ Intermediate SQL

**What the job requires:** "Intermediate SQL"

**Why Moura requires it:** All Moura operations (production, sales, inventory) are in PostgreSQL databases. You need to query, update, and automate data.

**How it works:**

SQL is the language for relational databases. "Intermediate" means you master:

| Operation | What it does | Example |
|-----------|-------------|---------|
| `SELECT ... JOIN` | Join data from 2+ tables | `SELECT * FROM sales JOIN products` |
| `GROUP BY` + `SUM/AVG` | Aggregate by category | `SUM(value) GROUP BY region` |
| `WHERE` with subquery | Filter based on another query | `WHERE id IN (SELECT id FROM ...)` |
| `WITH` (CTE) | Temporary table for complex queries | `WITH sales_2024 AS (...)` |
| `RANK() OVER` | Window function for ranking | `RANK() OVER (ORDER BY revenue DESC)` |

> **CTE** vs **Subquery**: Both do similar things, but CTE is more readable. A subquery is nested inside `WHERE`/`FROM`; a CTE is defined beforehand with `WITH`.

**Stored Procedure — how it works:**

A saved SQL block that runs on the database server:

```sql
CREATE PROCEDURE finish_order(id INT, qty INT)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE production_orders SET status = 'done', quantity = qty WHERE id = id;
END;
$$;

CALL finish_order(1, 500);
```

**Trigger — how it works:**

Automatically fires when an INSERT, UPDATE, or DELETE occurs:

```sql
CREATE TRIGGER trg_validate_qty
BEFORE INSERT ON production_orders
FOR EACH ROW
EXECUTE FUNCTION validate_quantity();
```

**View — how it works:**

A **view** is a "saved query". You use `SELECT * FROM view` as if it were a table, but underneath it executes the query. Useful for avoiding repeated complex queries.

```sql
-- Create view
CREATE VIEW vw_top_products AS
SELECT p.name, SUM(s.total_value) as revenue
FROM sales s JOIN products p ON s.product_id = p.product_id
GROUP BY p.name ORDER BY revenue DESC;

-- Use (same syntax as table)
SELECT * FROM vw_top_products WHERE revenue > 10000;
```

**What was implemented:**

| File | Objects | Lines |
|------|---------|-------|
| `01_schema.sql` | 4 tables, 7 indexes | Full schema |
| `02_queries.sql` | 8 analytical queries | KPIs, rankings, trends |
| `03_procedures.sql` | 4 procedures + 3 tables | Process automation |
| `04_triggers.sql` | 4 triggers | Validation, audit, logging |
| `05_analytics.sql` | 5 analytical views | Performance, health, forecast |

---

### 3. 📋 BPM (Business Process Management)

**What the job requires:** "BPM knowledge — Map and document process flows"

**BPM is NOT an app.** BPM is a **management methodology** (Business Process Management). It's the practice of understanding, documenting, analyzing, and improving processes.

**BPMN** is the **language/notation** used to draw these processes. Think of it as a universal flowchart language that any company understands.

**Tools that use BPMN:** Bizagi Modeler (free), Azure Logic Apps, Camunda, Visio. `.bpmn` files are XML that these tools can open.

**Why Moura requires it:** Moura needs to document and standardize processes (sales, production, support). Before automating with code, you need to draw the flow in BPMN.

**Sales process example in BPMN:**

```
START → [Validate Order] → DECISION: Is order valid?
  │ YES                          │ NO
  ▼                              ▼
[Check Stock]               [Reject Order]
  │                              │
  ▼                              ▼
[Create Production Order]   END (Rejected)
  │
  ▼
[Invoice Order]
  │
  ▼
END (Completed)
```

BPMN symbols you need to know:
| Symbol | Name | Meaning |
|--------|------|---------|
| ○ | Start Event | Where the process begins |
| □ | Task | Activity done by person or system |
| ◇ | Gateway | Decision point (e.g., "valid? yes/no") |
| ● | End Event | Where the process ends |
| → | Sequence Flow | Arrow showing the flow |

**What was implemented:**
- `docs/bpmn/sales_process.bpmn` — BPMN 2.0 XML with 2 gateways, 5 tasks
- `docs/bpmn/support_process.bpmn` — IT support flow (N1 → N2 → N3 triage)
- To view: open in **Bizagi Modeler** (free) or any BPMN editor

---

### 4. 🌐 IT Fundamentals

**What the job requires:** "IT Fundamentals (Networks, Information Security, OS)"

**How it works in the project:**

**Networks:** FastAPI runs on port 8000 (localhost). When deployed, uses HTTPS on port 443. PostgreSQL uses port 5432. Communication is TCP/IP.

```
[Browser] --HTTPS--> [FastAPI :8000] --TCP--> [PostgreSQL :5432]
```

**Security:**
- Credentials stay in `.env` (never in source code)
- `CORS` configured to prevent malicious site access
- Input validation on all endpoints (Pydantic models)
- `.gitignore` excludes `.env` from versioning

**Explanation of technical terms:**

| Term | Explanation |
|------|------------|
| **Network** | Set of connected computers that exchange data. The internet is the largest network |
| **TCP/IP** | Standard internet protocol. Splits data into packets and ensures they reach the destination |
| **HTTP/HTTPS** | Protocol your browser uses to access websites. HTTPS is the encrypted version |
| **Port** | "Logical port" — number identifying which service is running. E.g., port 80 = web, 443 = HTTPS, 5432 = PostgreSQL, 8000 = our API |
| **localhost** | Address `127.0.0.1` — your own computer. When you access `localhost:8000`, you're accessing a server on your machine |
| **Firewall** | Program that blocks unauthorized connections |
| **CORS** | Browser security mechanism that prevents malicious sites from accessing your API |
| **.env** | File storing **environment variables** (passwords, API keys). Never committed to GitHub |
| **Docker** | Tool that creates "containers" — isolated environments with everything needed to run the project |

**OS:** Compatible with Windows (PowerShell), Linux (bash), and macOS (zsh).

---

### 5. ⚡ Power Platform

**What the job requires:** "Power Platform (Power Automate, Power BI)"

**Power Platform is NOT a single app.** It's a **suite of Microsoft tools** called a "low-code platform". It includes:

**Power Automate** → automates repetitive tasks
**Power BI** → creates dashboards and reports
**Power Apps** → creates mobile/desktop apps
**Power Virtual Agents** → creates chatbots

---

**Power Automate** — What is it?
It's a **web service** (https://make.powerautomate.com) where you create **automation flows** without coding. You use visual blocks like LEGO:

```
📌 TRIGGER (starts the flow):
   "When a new row is inserted in production_orders table"

   ⬇️

🔧 CONDITION:
   "If total_value > 50,000"
   │
   ├── YES 📧 "Send email to manager: 'Approve order #123'"
   │
   └── NO ✅ "Update status to 'auto-approved'"
```

**Power BI** — What is it?
It's an **app/service** (https://app.powerbi.com) for creating **interactive dashboards**. It connects to databases (PostgreSQL, SQL Server) and creates charts using DAX measures.

**DAX** is the formula language of Power BI. Real examples from the project:

```dax
// Measure: Year-to-date revenue
Revenue YTD = TOTALYTD(SUM(sales[value]), calendar[Date])

// Measure: Gross margin percentage
Margin = DIVIDE([Revenue] - [Cost], [Revenue])

// Measure: Average ticket per sale
Avg Ticket = DIVIDE(SUM(sales[value]), COUNTROWS(sales))
```

**What was implemented:**
- `power-platform/power-automate/` — 2 documented flows (approval + notification)
- `power-platform/power-bi/` — 12 DAX measures + dashboard layout (4 tabs)
- `power-platform/power-apps/` — Mobile app with 5 documented screens

---

### 6. 📊 Azure Boards

**What the job requires:** "Azure Boards"

**Azure Boards IS a web app.** It's a **website** inside Azure DevOps (https://dev.azure.com) that IT teams use to **organize tasks**.

Inside Azure Boards, you create **Work Items** — cards representing tasks:

| Type | What it is | Example |
|------|-----------|---------|
| Epic | Large project | "Moura Automation System" |
| Feature | Functionality | "REST API for processes" |
| Story (US) | User need | "As an analyst, I want to create processes via API" |
| Task | Technical task | "Create POST /api/processes endpoint" |
| Bug | Error to fix | "GET endpoint returns 500 without auth" |

Each item has: **priority**, **assignee**, **story points** (effort), **status** (To Do / Doing / Done).

**Visual hierarchy:**

```
📁 Epic: Automation System
 └── 📋 Feature: REST API
      ├── 📝 Story: Process CRUD (8 pts)
      │    ├── 🔧 Task: GET endpoint (2 pts)
      │    ├── 🔧 Task: POST endpoint (2 pts)
      │    └── 🔧 Task: Tests (2 pts)
      └── 📝 Story: SAP Integration (5 pts)
```

**What was implemented:**
- `agile/azure-boards/backlog.md` — complete backlog: 5 sprints, 22 items (epics, stories, tasks)
- `agile/azure-boards/sprint_planning.md` — planning template with DoD, daily scrum, burndown

---

### 7. 📝 Requirements Analysis

**What the job requires:** "Develop requirements analysis and technical specification"

**How it works:** The process of discovering WHAT the system must do. Involves interviewing users, documenting features (FR), constraints (NFR), and business rules (BR).

**What was implemented:**

**Functional Requirements (FR):** The system MUST do X
- FR01: Process CRUD
- FR02: Dashboard with KPIs
- FR03: Predictive ML
- FR04: Generative AI
- FR05: System integration
- FR06: ETL pipeline

**Non-Functional Requirements (NFR):** The system MUST BE X
- NFR01: Performance (< 500ms)
- NFR02: Security (validation, .env)
- NFR03: Availability (99.9%)

**Business Rules (BR):**
- BR01: Quantity > 0 and ≤ 100,000
- BR02: Corrective maintenance triggers alert
- BR03: Report only with consolidated data

**Files:** `docs/requisitos/requirements_analysis.md` + `docs/requisitos/user_stories.md`

---

### 8. 📐 Technical Specification

**What the job requires:** "Technical specification"

**How it works:** Document that translates requirements into technical decisions: technologies, architecture, endpoints, database.

**What was implemented:** `docs/especificacao_tecnica.md` with architecture, stack, endpoints, schema, execution instructions.

---

### 9. 🏃 Agile Methodologies

**What the job requires:** "Agile Methodologies"

**How it works:** Scrum divides work into **sprints** (2-week cycles). Each sprint has:
- **Planning:** team decides what to do
- **Daily:** 15min standup meeting
- **Review:** demonstrate what was built
- **Retro:** continuous improvement

**What was implemented:** `agile/scrum-guide.md` with roles, ceremonies, artifacts, estimation.

---

### 10. 🔗 System Integration

**What the job requires:** "Analyze and fix system integration"

**How it works:** Integration connects two systems for data exchange. Most common pattern: **REST API** — one system sends an HTTP request, the other responds with JSON.

```
SAP ──POST /sync──→ Middleware ──INSERT──→ PostgreSQL
                     ↓ log
              log_operations table
```

**Implemented endpoints:**

```bash
# Sync SAP → Power BI
curl -X POST http://localhost:8000/api/integration/sync \
  -H "Content-Type: application/json" \
  -d '{"source_system":"sap","target_system":"powerbi","payload":{"items":[]}}'

# Response:
# {"status":"success","sync_id":"a1b2c3","records_processed":150}
```

**What was implemented:**
- `src/python/api/routers/integration.py` — 3 endpoints
- `docs/api_integration.md` — guide with examples
- Audit log in `producao.log_operacoes`

---

### 11. 🔄 ETL / ELT

**What the job requires:** "Develop Data projects (ETL and ELT)"

**How it works:**

**ETL = Extract + Transform + Load**

```
CSV/JSON files → EXTRACT (read) → TRANSFORM (clean) → LOAD (save)
    data/sample/      pandas           fill NA,        PostgreSQL
                                       rename,          Parquet
                                       type cast
```

**Each step in code:**

```python
# EXTRACT: read CSV files from directory
df = pd.concat([pd.read_csv(f) for f in csv_files])

# TRANSFORM: clean data
df = df.fillna(0)
df.columns = [c.strip().lower() for c in df.columns]
df["date"] = pd.to_datetime(df["date"])

# LOAD: save as Parquet (Gold layer)
df.to_parquet("gold/sales.parquet")
```

**Explanation of technical terms:**

| Term | Explanation |
|------|------------|
| **ETL** | **Extract, Transform, Load** — process of taking raw data, cleaning it, and saving in a ready-to-analyze format |
| **ELT** | Same idea but Transformation happens **after** loading into the database. More used in Big Data |
| **pandas** | Python library for working with table data (DataFrame). Reads CSV, Excel, SQL, JSON |
| **DataFrame** | In-memory table in Python. Rows and columns, like Excel |
| **Parquet** | File format **faster and more compact** than CSV. Stores binary data (not text). PySpark and Power BI read it directly |
| **Gold Layer** | Final data layer — data ready for consumption (reports, dashboards, ML) |
| **Silver Layer** | Cleaned and standardized data, but not yet aggregated |
| **Bronze Layer** | Raw data as it arrived (original CSV, raw log) |
| **SQLAlchemy** | Library that connects Python to SQL databases (PostgreSQL, MySQL, SQLite). Allows writing SQL directly or using ORM |

**What was implemented:**
- `src/python/data/etl_pipeline.py` — complete pipeline with 6 operations
- `src/python/data/validators.py` — 7 validators (missing, outliers, types, etc.)
- `src/python/data/database.py` — SQLAlchemy connection

---

### 12. 📊 Dashboards

**What the job requires:** "Develop dashboards"

**How it works:** A dashboard collects data from multiple sources and presents it in charts and KPIs. Streamlit auto-reloads when code changes.

**Streamlit Dashboard — actual screen:**
```
┌─────────────────────────────────────────────────────┐
│ R$ 2.4M   12,500 units    89.2%     4 products      │
│ ┌─────────────────────────────────────────────────┐ │
│ │           Interactive Plotly chart              │ │
│ │  ▁▂▃▅▇▆▅▆▇▆▅▃▂▁                                 │ │
│ └─────────────────────────────────────────────────┘ │
│ Tab1: Time Series | Tab2: Distribution              │
│ Tab3: ML Predictions | Tab4: AI Report              │
└─────────────────────────────────────────────────────┘
```

**What was implemented:**
- `src/python/dashboard/app.py` — Streamlit with Plotly
- `power-platform/power-bi/dax_measures.md` — 12 DAX measures

---

### 13. 🤖 Machine Learning — Classification

**What the job requires:** "Train ML models (classification)"

**How it works:** RandomForest builds multiple decision trees. Each tree "votes" on the class. The majority vote wins.

```
Features: [temp, vibration, pressure, hours, load]
    ↓
RandomForest with 100 trees
    ↓
Result: 0 (normal) or 1 (risk) + probability
    ↓
Feature importance: vibration: 0.35, temperature: 0.28, ...
```

**Metrics:**
- **Accuracy:** % correct overall
- **Precision:** when it says "risk", how often it's right
- **Recall:** of actual risks, how many were detected
- **F1-score:** harmonic mean of precision and recall

**Explanation of technical terms:**

| Term | Explanation |
|------|------------|
| **Classification** | ML type that predicts a **category** (e.g., "fail yes or no?", "customer A, B or C?") |
| **RandomForest** | Algorithm that builds **multiple decision trees** and combines the result. Like asking 100 experts and averaging |
| **Feature** | Model input column (e.g., temperature, vibration, pressure). The model learns patterns from them |
| **Target** | Column we want to predict (e.g., 0 = machine normal, 1 = machine will fail) |
| **Feature Importance** | The model tells which feature **most impacts** the decision. E.g., "vibration is 2x more important than temperature" |

**What was implemented:** `src/python/ml/classifier.py`

---

### 14. 📈 Machine Learning — Regression

**What the job requires:** "Train ML models (regression)"

**How it works:** Instead of classes, regression predicts a **continuous number**. RandomForestRegressor averages predictions from all trees.

```
Features: [temperature, humidity, speed, quality]
    ↓
RandomForestRegressor
    ↓
Predicted efficiency: 87.3%
```

**Metrics:**
- **RMSE:** average error (in variable units)
- **MAE:** mean absolute error
- **R²:** how much variance the model explains (0 to 1)

**What was implemented:** `src/python/ml/regressor.py`

---

### 15. 🔬 Machine Learning — Clustering

**What the job requires:** "Train ML models (clustering)"

**How it works:** KMeans groups data into K clusters. Each group has a **centroid** (center point). Data points are assigned to the nearest centroid.

```
Raw data:           After KMeans (K=3):
   ↑                        ██  ○○
   │   ○○              ██  ○○
   │  ○○  ██     →     ██  ○○  □□
   │ □□  ██  ○○             □□
   │ □□  ██  ○○             □□
   └─────────→         └─────────→
                      Cluster 0: efficient machines
                      Cluster 1: stressed machines
                      Cluster 2: idle machines
```

**Explanation of technical terms:**

| Term | Explanation |
|------|------------|
| **Clustering** | ML type that **groups similar data** without supervision (no need for correct answers to train) |
| **KMeans** | Algorithm that divides data into K groups. Each group has a center (centroid). Each point belongs to the nearest centroid |
| **Centroid** | Center point of a cluster. Average of all points in that group |
| **K** | Number of groups you want to find (in the project: K=3) |
| **Silhouette Score** | Measures how well-separated the clusters are. Ranges from -1 to 1. Closer to 1 is better |

**Difference between Classification and Clustering:**

| Classification (item 13) | Clustering (item 15) |
|------------------------|----------------------|
| Needs labeled data to train | Does not need labels |
| You define categories beforehand | The algorithm discovers the groups |
| E.g., "Is this SPAM or not?" | E.g., "Which customers are similar?" |

**What was implemented:** `src/python/ml/clustering.py`

---

### 16. 🧮 Feature Engineering

**What the job requires:** "Perform feature engineering"

**How it works:** Create new columns from existing data to improve model accuracy.

**Practical example:**
```
Original date: 2024-01-15
Generated features:
  → year: 2024
  → month: 1
  → day_of_week: 2 (Tuesday)
  → is_weekend: 0
  → quarter: 1

Yesterday's production: 100 units
  → lag_1: 100 (previous day's production)
  → rolling_mean_7: 95 (7-day average)
```

**Explanation of technical terms:**

| Technique | Explanation | Example |
|-----------|------------|---------|
| **Time features** | Extract information from a date | `2024-01-15` → year, month, day, day_of_week, is_weekend, quarter |
| **Lag** | Use yesterday's value to predict today | `lag_1` = yesterday's production. `lag_7` = 7 days ago |
| **Rolling window** | Moving average of a period | `rolling_mean_7` = average of last 7 days. `rolling_std_7` = standard deviation |
| **Aggregate features** | Statistics by group | Per machine: average production, std dev, min, max |
| **One-hot encoding** | Transform category into 0/1 columns | Shift: `morning=[1,0,0]`, `afternoon=[0,1,0]`, `night=[0,0,1]` |
| **Label encoding** | Transform category into numbers 1,2,3 | Shift: `morning=1`, `afternoon=2`, `night=3` |
| **Interaction** | Multiply two features | `temperature * vibration` — may reveal patterns each feature alone doesn't show |

**What was implemented:** `src/python/ml/feature_engineering.py` — 6 feature creation methods.

---

### 17. 🌐 LLMs via API

**What the job requires:** "Integrate LLM APIs; familiarity with LLMs via API"

**How it works:** LLMs (GPT-4, Claude) receive text (prompt) and generate new text. Communication is via REST API:

```
[Your code] ──HTTP POST──→ [OpenAI API]
  Prompt: "Generate a report..."       |
  ←── Response: "## Report..." ────────┘
```

```python
from openai import OpenAI
client = OpenAI(api_key="sk-...")
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Explain BPMN"}]
)
print(response.choices[0].message.content)
```

**Explanation of technical terms:**

| Term | What it is |
|------|------------|
| **LLM** | Large Language Model — AI model trained on billions of texts to generate and understand natural language |
| **OpenAI API** | Pay-per-use service that sends prompts to GPT models via HTTP requests |
| **GPT** | Generative Pre-trained Transformer — model architecture created by OpenAI |
| **Token** | Text unit processed by LLMs (1 token ≈ 0.75 English word). Cost is per token |
| **Chat Completion** | API format where you send a message list (system, user, assistant) and receive a response |
| **Temperature** | Parameter controlling creativity: 0 = always same answer, 1 = more creative/random |
| **Model** | Specific GPT version (e.g., gpt-4o-mini is faster/cheaper than gpt-4o) |

**What was implemented:** `src/python/llm/client.py` — configurable OpenAI / Azure OpenAI client.

---

### 18. 🎯 Prompt Engineering

**What the job requires:** "Basic prompt engineering"

**How it works:** Response quality depends on prompt quality. Basic rules:

| Rule | Bad | Good |
|------|-----|------|
| Be specific | "Generate a report" | "Generate a technical report with: summary, KPI analysis, 3 recommendations" |
| Give context | "Analyze this" | "Analyze this feedback sentiment: 'The system is slow'" |
| Define format | "Answer" | "Respond in JSON with: sentiment, confidence" |

**What was implemented:** `src/python/llm/prompts.py` — 3 templates with best prompting practices.

---

### 19. 🧠 Generative AI

**What the job requires:** "Implement basic solutions with generative AI"

**How it works:** Generative AI **creates** new content (text, code). Different from discriminative AI that only classifies or predicts.

**Report generation pipeline:**
```
Dashboard KPIs → JSON Summary → LLM Prompt → Text Report
                     ↓                          ↓
             {"revenue": 2400000,         "## Executive Summary
              "efficiency": 89.2,          In the analyzed period..."
              "failure_rate": 3.5}
```

**What was implemented:** `src/python/llm/generators.py` — 3 generators with offline fallback.

---

### 20. 🎫 Ticket Management

**What the job requires:** "Ticket management and performance metrics monitoring"

**Support flow (BPMN):**

```
[Ticket Opened] → [Triage]
    ↓ N1 (basic)           ↓ N2 (analyst)
[Support resolves]   [Analyst investigates]
    ↓                     ↓
    └──◇ Resolved?──┘
        Yes → [Ticket Closed] + [Log]
        No → [Escalate N3]
```

**Monitoring:** `GET /health` endpoint returns API status and database connection.

---

### 21. 👨‍🏫 User Training

**What the job requires:** "User training on system usage"

**What was implemented:** `docs/user_training.md` — complete guide with modules, commands, common errors, and FAQ.

---

### 22. 🇬🇧 Technical English

**What the job requires:** "Technical English (reading)"

**Applied in project:** Code uses English names (variables, functions, classes). Documentation alternates PT-BR (explanations) with EN (technical terms: endpoint, payload, feature, pipeline).

---

### 23. 💻 .NET / C#

**What the job requires:** "Knowledge of .NET, C#"

**How it works:** ASP.NET Core creates APIs using **Controller → Service** pattern. The Controller receives the HTTP request, calls the Service (business logic), and returns the response.

```
HTTP GET /api/process → ProcessController.GetAll()
                          → ProcessService.GetAll()
                              ← List<ProcessModel>
                          ← JSON
```

**Explanation of technical terms:**

| Term | What it is |
|------|------------|
| **.NET** | Microsoft's development platform for Windows, Web, and API applications |
| **ASP.NET Core** | .NET's web framework for creating APIs and websites. Runs on Windows, Linux, macOS |
| **C#** | Main .NET programming language. Compiled, typed, object-oriented |
| **Controller** | Class that receives HTTP requests and defines endpoints. E.g., `ProcessController.Get()` |
| **Service** | Class containing business logic. Controller calls Service, which processes and returns data |
| **Swagger / OpenAPI** | Web interface that documents and tests API endpoints automatically. Accessible at `/swagger` |
| **DTO** | Data Transfer Object — simple object that carries data between layers (Controller → Service) |
| **Dependency Injection** | Pattern where the framework automatically creates and injects dependencies (e.g., Service into Controller) |

**What was implemented:** `src/dotnet/ProcessAutomation.Api/` — 6 endpoints, Swagger.

---

### 24. 🌐 JavaScript

**What the job requires:** "Knowledge of JavaScript"

**How it works:** The frontend uses `fetch()` to call the API and renders results in the DOM.

```javascript
const api = new MouraApiClient('http://localhost:8000');
const processes = await api.getProcesses();
// render in HTML table
```

**Explanation of technical terms:**

| Term | What it is |
|------|------------|
| **DOM** | Document Object Model — tree representation of HTML that JavaScript manipulates to change the page |
| **Chart.js** | JavaScript library for creating interactive charts (bar, pie, line) in HTML canvas |
| **Fetch API** | Native JavaScript function for HTTP requests (GET, POST, PUT, DELETE) |
| **async/await** | Modern syntax for handling async operations (API calls, files) without blocking the page |
| **Promise** | Object representing an operation that hasn't completed yet. `await` "waits" for the Promise |
| **Arrow Function** | Shorter function syntax: `(x) => x * 2` instead of `function(x) { return x * 2 }` |

**What was implemented:** `src/javascript/` — Dashboard with Chart.js, CRUD, integration.

---

### 25. 📜 SAP Scripts

**What the job requires:** "Knowledge of SAP Scripts"

**How it works:** SAP GUI allows automation via VBScript. The script controls the SAP interface like a user (fills fields, clicks buttons).

```vbscript
' Example: open transaction, fill field, execute
Session.findById("wnd[0]/tbar[0]/okcd").text = "/nVA03"
Session.findById("wnd[0]/usr/ctxtVBAK-VBELN").text = "10000001"
Session.findById("wnd[0]").sendVKey 0
```

**Explanation of technical terms:**

| Term | What it is |
|------|------------|
| **SAP GUI** | Desktop program that connects to the SAP server and shows the system interface (fields, buttons, screens) |
| **VBScript** | Microsoft scripting language (Visual Basic Scripting) that automates Windows programs |
| **Transaction Code** | Code that opens a specific SAP screen. E.g., `/nVA03` = display sales order |
| **Session** | Object representing the current SAP GUI window. All automation starts with `Session.findById(...)` |
| **BAPI** | Business API — official SAP function for system integration (more stable than GUI automation) |
| **RFC** | Remote Function Call — SAP communication protocol for calling remote functions |
| **sendVKey** | Command that simulates pressing a key in SAP (Enter, F8 = execute, F3 = back) |

**What was implemented:** `sap/sap_scripts.md` — 3 scripts + Python integration.

---

### 26. 🎨 FIGMA

**What the job requires:** "Knowledge of FIGMA"

**What was implemented:** `figma/` — Design system (colors, typography, components) + 5 screen wireframes described in markdown.

---

### 27. 📊 Bizagi

**What the job requires:** "Knowledge of Bizagi"

**What was implemented:** `docs/bpmn/*.bpmn` — BPMN 2.0 files openable in Bizagi Modeler (free) for visual editing.

---

## 🚀 Running the project

```bash
# 1. API (http://localhost:8000/docs)
uvicorn src.python.api.main:app --reload --port 8000

# 2. Dashboard (http://localhost:8501)
streamlit run src/python/dashboard/app.py

# 3. JS Frontend (http://localhost:3000)
cd src/javascript && npx http-server src -p 3000

# 4. .NET API (http://localhost:5000/swagger)
cd src/dotnet && dotnet run --project ProcessAutomation.Api

# 5. Tests
pytest tests/ -v
```

---

## 🏗️ Project structure

```
src/python/      → API + automation + ML + LLM + ETL + dashboard
src/dotnet/      → C# API
src/javascript/  → Frontend
sql/             → 5 SQL files (schema → analytics)
docs/            → Requirements, BPMN, specification, training
power-platform/  → Automate, BI, Apps
agile/           → Scrum, Azure Boards
figma/           → Design system, wireframes
sap/             → SAP scripts
tests/           → Python + SQL tests
```

---

> Portfolio project for the **Junior IT Development Analyst — Grupo Moura** position.
