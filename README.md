# moura-stack-training

# Moura Stack – FastAPI + Streamlit + Power BI + ETL (Prefect/Spark) + ML/Stats + Postgres + dbt

## O que cobre (match com a vaga)
- **SQL (consultas, triggers, procedures)**: `sql/01_init.sql` + API lendo Postgres via SQLAlchemy.
- **Dashboards/relatórios**: Streamlit + Plotly/Matplotlib/Seaborn + export Excel.
- **Power BI Service**: embed via `POWER_BI_EMBED_URL`; endpoint `/gold/export` gera **Parquet/CSV** (camada **Gold**).
- **Automação**: endpoint `/etl/run` (webhook p/ **Power Automate**) dispara **Prefect**.
- **Python (bibliotecas)**: pandas, numpy, SciPy, Statsmodels, scikit-learn.
- **Big Data**: job **PySpark** (`app/etl/spark_job.py`) gerando Parquet.
- **dbt**: projeto mínimo `dbt/` com `stg_sales` (silver) e `fct_sales` (gold).

## Setup
```bash
python -m venv .venv
. .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
