# Moura-Stack-Training

## 🌐 [English Version of README](README_EN.md)

# Moura Stack – FastAPI + Streamlit + Power BI + ETL (Prefect/Spark) + ML/Stats + Postgres + dbt

Projeto-portfólio para uma vaga de **Estágio/Dev no Grupo Moura**, demonstrando ponta a ponta: **APIs** em FastAPI, **dashboard** em Streamlit, **SQL avançado** (consultas, trigger e procedure em PostgreSQL), **embed de Power BI**, **ETL** com Prefect e job **PySpark** (Big Data), **camada Gold** (Parquet/CSV), modelos **dbt** (silver/gold), análises com **Pandas/NumPy/SciPy/Statsmodels**, e um **modelo de regressão** com Scikit-learn. Inclui endpoints para automação (**/etl/run**) e exportação da camada Gold (**/gold/export**), testes, lint e Docker.

---

## 🔨 Funcionalidades do Projeto
- **Backend (FastAPI)**  
  - Rotas: `/health`, `/metrics/sales`, `/metrics/summary`, `/stats/pearson`, `/stats/ols`, `/ml/train`, `/ml/predict`, `/etl/run`, `/gold/export`.  
  - **PostgreSQL**: conexão via SQLAlchemy; **tabela `sales`** com **trigger** (`set_total`) e **procedure** (`upsert_product_revenue`) em `sql/01_init.sql`.
- **Frontend (Streamlit)**  
  - Tabela de amostra, KPIs, **gráficos Plotly** (interativo) e **Seaborn/Matplotlib** (estático).  
  - Embed de **Power BI** via `POWER_BI_EMBED_URL`.  
  - Botões para rodar **Pearson/OLS**, **treinar/predizer** (Scikit-learn), disparar **ETL** e **export Gold**.
- **ETL & Big Data**  
  - **Prefect**: `app/etl/flow_etl.py` gera **Parquet** (camada Gold).  
  - **PySpark**: `app/etl/spark_job.py` (opcional) processa CSV → Parquet com cálculo de `total`.
- **Analytics & ML**  
  - **SciPy** (correlação Pearson), **Statsmodels** (OLS), **Scikit-learn** (Regressão Linear).  
  - **OpenPyXL** para export Excel a partir do Streamlit.
- **dbt (Mínimo Viável)**  
  - `stg_sales` (silver) e `fct_sales` (gold) em `dbt/models/`.  
- **Operacional**  
  - Testes `pytest`, lint `ruff`, formatador `black`, **Dockerfile** e **docker-compose**.

---

### 📸 Exemplo Visual do Projeto
<div align="center">
  <img src="docs/screenshot-dashboard-1.png" alt="Streamlit Dashboard - KPIs e Tabela" width="80%" style="margin: 16px 0; border-radius: 10px;">
  <img src="docs/screenshot-dashboard-2.png" alt="Gráficos Plotly e Seaborn" width="80%" style="margin: 16px 0; border-radius: 10px;">
</div>

> Dica: substitua os caminhos das imagens acima por capturas reais do seu ambiente.

---

## ✔️ Técnicas e Tecnologias Utilizadas
- **Linguagem:** Python 3.11+  
- **Backend:** FastAPI, Pydantic, Uvicorn, SQLAlchemy  
- **Banco de Dados:** PostgreSQL (psycopg2) — **consultas, trigger e procedure**  
- **Frontend/BI:** Streamlit, **Power BI embed**  
- **Dados/Análises:** Pandas, NumPy, Plotly, Matplotlib, Seaborn, SciPy, Statsmodels  
- **ML:** Scikit-learn (regressão linear)  
- **ETL/Big Data:** Prefect, PySpark, Parquet (PyArrow)  
- **Modelagem de Dados:** dbt (silver/gold)  
- **Dev/Qualidade:** pytest, requests, Ruff, Black, Docker

---

## 📁 Estrutura do Projeto
```

moura-stack/
├─ app/
│  ├─ backend/
│  │  ├─ main.py               # FastAPI app / CORS / include\_routers
│  │  ├─ db.py                 # engine, SessionLocal, ping()
│  │  ├─ models.py             # Schemas Pydantic (SalesRecord, Summary, ML, Stats)
│  │  └─ routers/
│  │     ├─ health.py          # /health
│  │     ├─ metrics.py         # /metrics/sales, /metrics/summary
│  │     ├─ stats.py           # /stats/pearson, /stats/ols
│  │     ├─ ml.py              # /ml/train, /ml/predict
│  │     ├─ etl.py             # /etl/run (webhook p/ Automate)
│  │     └─ gold.py            # /gold/export (Parquet/CSV)
│  ├─ frontend/
│  │  └─ streamlit\_app.py      # Dashboard, gráficos, ações
│  └─ etl/
│     ├─ flow\_etl.py           # Prefect flow (CSV/Postgres → Parquet)
│     └─ spark\_job.py          # ETL PySpark opcional
├─ data/
│  ├─ sample\_sales.csv
│  └─ processed/               # saída Parquet/CSV (Gold)
├─ dbt/
│  ├─ dbt\_project.yml
│  └─ models/
│     ├─ schema.yml
│     ├─ stg\_sales.sql         # silver
│     └─ fct\_sales.sql         # gold
├─ sql/
│  └─ 01\_init.sql              # tabela, trigger e procedure (Postgres)
├─ tests/
│  ├─ test\_api.py
│  └─ test\_stats\_ml.py
├─ .env.example
├─ requirements.txt
├─ pyproject.toml
├─ Dockerfile
├─ docker-compose.yml
└─ README.md

````

---

## 🛠️ Abrir e rodar o projeto

### 1) Pré-requisitos
- **Python 3.11+**
- **PostgreSQL** (se for usar DB real)
- (Opcional) **Docker** e **Docker Compose**
- (Opcional p/ Spark) **Java 17**

### 2) Clonar e configurar
```bash
git clone <URL_DO_REPOSITORIO>
cd moura-stack
python -m venv .venv
. .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
````

Edite `.env`:

* Para **CSV** (default): mantenha `ETL_SOURCE=csv`.
* Para **Postgres**:

  * `DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/dbname`
  * `ETL_SOURCE=postgres`

### 3) Banco (PostgreSQL)

Execute o script:

```bash
# Via psql ou cliente de sua preferência
# psql "postgresql://user:pass@host:5432/dbname" -f sql/01_init.sql
```

Isso cria **sales**, a **trigger** `set_total` e a **procedure** `upsert_product_revenue`, além de amostras.

### 4) Backend (FastAPI)

```bash
uvicorn app.backend.main:app --reload --host 0.0.0.0 --port 8000
# http://localhost:8000/docs
```

### 5) Frontend (Streamlit)

```bash
export BACKEND_BASE_URL=http://localhost:8000
streamlit run app/frontend/streamlit_app.py --server.port 8501
# http://localhost:8501
```

### 6) ETL

* **Prefect (local):**

  ```bash
  python app/etl/flow_etl.py
  ```
* **Webhook p/ Power Automate:**

  ```bash
  curl -X POST http://localhost:8000/etl/run
  ```

### 7) Export Gold

```bash
curl -X POST http://localhost:8000/gold/export
# Gera Parquet/CSV em data/processed/
```

### 8) Spark (opcional)

```bash
python app/etl/spark_job.py
```

### 9) Testes e Qualidade

```bash
pytest
ruff check .
black .
```

---

## 🌐 Deploy

### Opção A — Docker local

```bash
docker compose up --build
```

* Sobe **API** e **Streamlit** nos ports definidos no `.env`.
* Para usar **Postgres externo**, aponte `DATABASE_URL` no `.env`.

### Opção B — Nuvem (resumo)

* **API**: conteinerize (Dockerfile já pronto) e suba em um serviço gerenciado (Railway, Render, Fly.io, Azure Web Apps, AWS ECS/Fargate).
* **Streamlit**: rodar como serviço separado (mesma imagem) ou migrar para framework web do seu stack.
* **Banco**: PostgreSQL gerenciado (Azure/AWS/GCP).
* **Power BI**: publicar o relatório e definir `POWER_BI_EMBED_URL`. Para **Embedded**, crie um endpoint de token (não incluso).
* **Automação**: conecte o **Power Automate** ao webhook `/etl/run`.
* **dbt**: aponte `profile` para o Postgres da nuvem e rode `dbt run`.

---

## ✅ Match com a vaga (resumo)

* **SQL (consultas, triggers, procedures)** → `sql/01_init.sql` + leitura via **SQLAlchemy**.
* **Dashboards/Relatórios** → **Streamlit** + **Plotly/Matplotlib/Seaborn** + export **Excel**.
* **Power BI Service** → **embed** + **/gold/export** (Parquet/CSV).
* **Automação** → webhook **/etl/run** acionável pelo **Power Automate**.
* **Python (bibliotecas)** → Pandas, NumPy, SciPy, Statsmodels, Scikit-learn.
* **Big Data** → **PySpark** gerando **Parquet**.
* **dbt (conceitos)** → `stg_sales` (silver) e `fct_sales` (gold).
