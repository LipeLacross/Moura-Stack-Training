## 🇧🇷 [Versão em Português](README.md)

# Moura-Stack-Training

Portfolio project showcasing **APIs (FastAPI)**, **dashboard (Jinja + Tailwind + Chart.js/Plotly/D3)**, **PostgreSQL SQL** (queries, *trigger*, *procedure*), **ETL (Prefect/pandas)**, **Big Data (PySpark)**, **exports (CSV/Parquet/Excel)**, and **analytics modeling (dbt)**, with optional **Power BI** embedding. The Dockerfile includes **Java 17** to enable Spark.

---

## 🔨 Project Features

* **REST API (FastAPI)**
  Ready-to-use endpoints:

  * `GET /` — Dashboard (Jinja)

  * `GET /api/sales` — Sales with filters, sorting, and pagination

  * `GET /api/summary` — KPIs (revenue, quantity, AOV, top products)

  * `GET /api/charts/revenue` — Time series (week/month/year)

  * `GET /api/charts/categories` — Top categories/products

  > **Note**: the dashboard template references `/metrics/*` for filters/preview. If you don’t expose the `metrics` routers, adjust the frontend to call `/api/*`.
* **Jinja Dashboard** with KPIs, paginated table, areas for interactive charts (Chart.js/Plotly/D3) and generated images (Matplotlib/Seaborn/Stats).
* **PostgreSQL**: `sales` table + example *trigger/procedure* in `sql/01_init.sql`.
* **ETL with Prefect/pandas**: CSV/Parquet (Gold layer) and utilities.
* **PySpark**: aggregation job (requires Java 17).
* **Excel Export**: export endpoint (in `extras` router when enabled).
* **dbt**: `stg_sales` (silver) and `fct_sales` (gold).
* **Infra**: Docker/Docker Compose ready.

---

### 📸 Visual Example of the Project

<div align="center">
  <img src="https://github.com/user-attachments/assets/e695f2c7-664c-40f1-8d81-005403694197" alt="Screen recording — dashboard demo" width="80%" style="margin: 16px 0; border-radius: 10px;">
</div>

---

## ✔️ Technologies

* **Language:** Python 3.11+
* **Backend:** FastAPI, Pydantic, Uvicorn, SQLAlchemy
* **Database:** PostgreSQL (psycopg2)
* **Frontend/BI:** Jinja + Power BI embed
* **Analytics:** pandas, NumPy, Plotly, Matplotlib, Seaborn, statsmodels, Chart.js, D3.js
* **ML:** scikit-learn (Linear Regression)
* **ETL/Big Data:** Prefect, PySpark, Parquet (PyArrow)
* **Data Modeling:** dbt
* **Dev/Quality:** Black, Docker

---

## 📁 Project Structure

* **app/backend/**

  * `main.py` — FastAPI app, static mount, dashboard, `/api/*` endpoints
  * `db.py` — engine/Session and simple health check
  * `models.py` — Pydantic schemas (Sales/Metric/Health, etc.)
* **app/core/**

  * `config.py` — (reserved for settings)
  * `utils.py` — `init_db_if_needed`, `ensure_sales_schema`, logging utils
* **app/services/**

  * `data.py`, `etl.py`, `metrics.py`, `ml.py`, `stats.py` — CSV/DB loading, KPIs, Pearson/OLS, train/predict
* **app/templates/**

  * `base.html`, `dashboard.html` — layout + filters + KPIs + table + charts
* **data/**

  * `sample_sales.csv` — sample dataset
* **dbt/**

  * `dbt_project.yml`, `models/stg_sales.sql`, `models/fct_sales.sql`
* **scripts/generate\_charts/**

  * `matplotlib_chart.py`, `plotly_chart.py`, `seaborn_chart.py`, `statistics_chart.py`, `ml_regression.py`, `pyspark_agg.py`
* **sql/**

  * `01_init.sql` — schema and SQL objects examples
* **public/**

  * `moura-logo.ico`, `moura-logo-1-2048x1651.png`, `matplotlib.png`, `plotly.png`, `seaborn.png`, `statistics.png`
* **Infra**

  * `Dockerfile`, `docker-compose.yml`, `requirements.txt`, `pyproject.toml`, `.env(.example)`

---

## 🛠️ Getting Started

1. **Prerequisites**

   * Python 3.11+
   * PostgreSQL
   * (Optional) Docker/Docker Compose
   * (Optional) Java 17 for PySpark (already included in Docker)

2. **Clone the Repository**

```bash
git clone <REPOSITORY_URL>
cd moura-stack-training
```

3. **Environment Setup**

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env`:

* `DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/dbname`
* `ETL_SOURCE=csv` (or `postgres`)
* `POWER_BI_EMBED_URL=` (optional)

> **Tip**: if you **don’t** have `sql/02_reset_sales.sql`, set `DB_AUTO_INIT=false` to avoid automatic reset attempts.

4. **Initialize the Database (base schema)**

```bash
psql "postgresql://user:pass@host:5432/dbname" -f sql/01_init.sql
```

5. **Run the Backend**

```bash
uvicorn app.backend.main:app --reload --port 8000
# Docs:      http://localhost:8000/docs
# Dashboard: http://localhost:8000/
```

6. **Dashboard (Jinja)**
   The home page `/` loads KPIs, table, and filters.

> **Heads-up**: if the frontend filters point to `/metrics/*`, switch them to `/api/*` (or add the corresponding routers).

7. **ETL & Exports (examples)**

```bash
curl -X POST http://localhost:8000/etl/run
curl -X POST http://localhost:8000/gold/export
curl -X POST http://localhost:8000/export/excel
```

8. **Run Spark (optional)**

```bash
python scripts/generate_charts/pyspark_agg.py
```

---

## 🌐 Deploy

* **Docker (local)**

```bash
docker compose up --build
```

* **Cloud**

  * **API**: publish the Docker image (Railway, Render, Fly.io, AWS ECS, etc.).
  * **Database**: use a managed PostgreSQL (RDS/CloudSQL/Azure).
  * **dbt**: point to the cloud Postgres and run `dbt run`.
  * **Power BI**: set `POWER_BI_EMBED_URL`.
