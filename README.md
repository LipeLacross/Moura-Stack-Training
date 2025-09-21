## 🌐 [English Version of README](README_EN.md)

# Moura-Stack-Training

Projeto desenvolvido para demonstrar competências técnicas (Moura) em **APIs (FastAPI)**, **dashboard em Jinja**, **SQL avançado em PostgreSQL** (consultas, trigger, procedure), **ETL com Prefect**, **Big Data com PySpark**, **exportações em Parquet/CSV e Excel**, além de **modelagem analítica com dbt**. O projeto também integra **Power BI embed**, estatística (Pearson/OLS) e machine learning (regressão linear com Scikit-learn).

---

## 🔨 Funcionalidades do Projeto

* **API REST (FastAPI)**
  Endpoints: `/health`, `/metrics/sales`, `/metrics/summary`, `/stats/pearson`, `/stats/ols`, `/ml/train`, `/ml/predict`, `/etl/run`, `/gold/export`, `/export/excel`, `/spark/run`.
* **Dashboard Jinja** com KPIs, gráficos interativos (Plotly) e estáticos (Matplotlib/Seaborn), Chart.js e D3.js.
* **Banco de Dados PostgreSQL**: tabela `sales`, trigger `set_total` e procedure `upsert_product_revenue`.
* **ETL com Prefect**: fluxo para gerar Parquet/CSV (camada Gold).
* **PySpark**: job para processamento em larga escala.
* **Export Excel**: endpoint usando OpenPyXL.
* **dbt**: modelos `stg_sales` (silver) e `fct_sales` (gold).
* **Infraestrutura**: Docker/Docker Compose prontos para uso.

---

### 📸 Exemplo Visual do Projeto

<div align="center">
  <img src="docs/screenshot-dashboard-1.png" alt="Screenshot 2025-07-03 132707" width="80%" style="margin: 16px 0; border-radius: 10px;">
  <img src="docs/screenshot-dashboard-2.png" alt="Screenshot 2025-07-03 130932" width="80%" style="margin: 16px 0; border-radius: 10px;">
</div>

---

## ✔️ Técnicas e Tecnologias Utilizadas

* **Linguagem:** Python 3.11+
* **Backend:** FastAPI, Pydantic, Uvicorn, SQLAlchemy
* **Banco de Dados:** PostgreSQL (psycopg2)
* **Frontend/BI:** Jinja + Power BI embed
* **Análises:** Pandas, NumPy, Plotly, Matplotlib, Seaborn, Statsmodels, Chart.js, D3.js
* **ML:** Scikit-learn (Regressão Linear)
* **ETL/Big Data:** Prefect, PySpark, Parquet (PyArrow)
* **Modelagem de Dados:** dbt
* **Dev/Qualidade:** Black, Docker

---

## 📁 Estrutura do Projeto

* **app/backend/**

  * `main.py`: instancia FastAPI, configurações e dashboard Jinja.
  * `db.py`: conexão com PostgreSQL via SQLAlchemy.
  * `models.py`: schemas Pydantic.
  * *(rotas organizadas em módulos importados pelo `main.py`)*.
* **app/core/**

  * `utils.py`: utilitários de inicialização/checagem de banco.
* **app/services/**

  * `data.py`: carregamento/transformações, métricas e modelos ML.
  * `etl.py`, `metrics.py`, `ml.py`, `stats.py`: serviços especializados.
* **app/templates/**

  * `base.html`: layout base.
  * `dashboard.html`: dashboard interativo.
* **data/**

  * `sample_sales.csv`: dados de exemplo.
* **dbt/**

  * `dbt_project.yml`: configuração.
  * `models/`

    * `stg_sales.sql`: camada silver.
    * `fct_sales.sql`: camada gold.
* **scripts/generate\_charts/**

  * `matplotlib_chart.py`, `plotly_chart.py`, `seaborn_chart.py`, `statistics_chart.py`, `ml_regression.py`, `pyspark_agg.py`.
* **sql/**

  * `01_init.sql`: criação de tabela, trigger e procedure.
* **public/**

  * `moura-logo.ico`: ícone do site.
  * `plotly.png`, `seaborn.png`, `statistics.png`, `matplotlib.png`, `moura-logo-1-2048x1651.png`.
* **Infraestrutura**

  * `requirements.txt`, `pyproject.toml`
  * `Dockerfile`, `docker-compose.yml`
  * `.env` e `.env.example`

---

## 🛠️ Abrir e rodar o projeto

Para iniciar o projeto localmente, siga os passos abaixo:

1. **Pré-requisitos**

   * Python 3.11+
   * PostgreSQL instalado
   * (Opcional) Docker/Docker Compose
   * (Opcional) Java 17 para PySpark

2. **Clone o Repositório**

```bash
git clone <URL_DO_REPOSITORIO>
cd moura-stack-training
```

3. **Configuração do ambiente**

```bash
python -m venv .venv
. .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Edite o `.env` e configure:

* `DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/dbname`
* `ETL_SOURCE=csv` ou `postgres`
* `POWER_BI_EMBED_URL=...`

4. **Rodar o Banco**

```bash
psql "postgresql://user:pass@host:5432/dbname" -f sql/01_init.sql
```

5. **Iniciar o Backend**

```bash
uvicorn app.backend.main:app --reload --port 8000
# http://localhost:8000/docs
```

6. **Dashboard Jinja**
   Abra no navegador:

```
http://localhost:8000/dashboard
```

7. **ETL & Exportações**

```bash
curl -X POST http://localhost:8000/etl/run
curl -X POST http://localhost:8000/gold/export
curl -X POST http://localhost:8000/export/excel
```

8. **Rodar Spark (opcional)**

```bash
python app/backend/spark_job.py
```

---

## 🌐 Deploy

* **Docker (local)**

```bash
docker compose up --build
```

* **Nuvem**

  * **API**: deploy via Docker em Railway, Render, Fly.io ou AWS ECS.
  * **Banco**: use PostgreSQL gerenciado (RDS, CloudSQL, Azure).
  * **Power BI**: configure `POWER_BI_EMBED_URL`.
  * **dbt**: aponte para o Postgres da nuvem e rode `dbt run`.

