## 🌐 [English Version of README](README_EN.md)

# Moura-Stack-Training

Projeto-portfólio para demonstrar competências em **APIs (FastAPI)**, **dashboard (Jinja + Tailwind + Chart.js/Plotly/D3)**, **SQL no PostgreSQL** (consultas, *trigger*, *procedure*), **ETL (Prefect/pandas)**, **Big Data (PySpark)**, **exportações (CSV/Parquet/Excel)** e **modelagem analítica (dbt)**, com embed opcional de **Power BI**. O Dockerfile já instala **Java 17** para habilitar o Spark.

---

## 🔨 Funcionalidades do Projeto

* **API REST (FastAPI)**
  Endpoints prontos:

  * `GET /` — Dashboard (Jinja)
  * `GET /api/sales` — Vendas com filtros, ordenação e paginação
  * `GET /api/summary` — KPIs (receita, quantidade, ticket médio, top produtos)
  * `GET /api/charts/revenue` — Série temporal (semana/mês/ano)
  * `GET /api/charts/categories` — Top categorias/produtos

  > **Nota**: o template do dashboard referencia `/metrics/*` para filtros/preview. Se você não publicar os *routers* de `metrics`, ajuste o front para usar os endpoints `/api/*`.
* **Dashboard Jinja** com KPIs, tabela paginada e áreas para gráficos interativos (Chart.js/Plotly/D3) e imagens geradas (Matplotlib/Seaborn/Stats).
* **Banco de Dados PostgreSQL**: tabela `sales` + exemplo de *trigger/procedure* no `sql/01_init.sql`.
* **ETL com Prefect/pandas**: geração de CSV/Parquet (camada Gold) e utilitários.
* **PySpark**: *job* de agregação pronto (requer Java 17).
* **Export Excel**: endpoint de exportação (em *router* `extras` quando habilitado).
* **dbt**: `stg_sales` (silver) e `fct_sales` (gold).
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
* **Análises:** pandas, NumPy, Plotly, Matplotlib, Seaborn, statsmodels, Chart.js, D3.js
* **ML:** scikit-learn (Regressão Linear)
* **ETL/Big Data:** Prefect, PySpark, Parquet (PyArrow)
* **Modelagem de Dados:** dbt
* **Dev/Qualidade:** Black, Docker

---

## 📁 Estrutura do Projeto

* **app/backend/**

  * `main.py` — app FastAPI, montagem de estáticos, dashboard, endpoints `/api/*`
  * `db.py` — engine/Session e *health* simples
  * `models.py` — *schemas* Pydantic (Sales/Metric/Health, etc.)
* **app/core/**

  * `config.py` — (reservado para *settings*)
  * `utils.py` — *init\_db\_if\_needed*, *ensure\_sales\_schema*, logs util
* **app/services/**

  * `data.py`, `etl.py`, `metrics.py`, `ml.py`, `stats.py` — carregamento CSV/DB, KPIs, Pearson/OLS, treino/predict
* **app/templates/**

  * `base.html`, `dashboard.html` — layout + filtros + KPIs + tabela + gráficos
* **data/**

  * `sample_sales.csv` — dataset de exemplo
* **dbt/**

  * `dbt_project.yml`, `models/stg_sales.sql`, `models/fct_sales.sql`
* **scripts/generate\_charts/**

  * `matplotlib_chart.py`, `plotly_chart.py`, `seaborn_chart.py`, `statistics_chart.py`, `ml_regression.py`, `pyspark_agg.py`
* **sql/**

  * `01_init.sql` — schema e exemplos de objetos SQL
* **public/**

  * `moura-logo.ico`, `moura-logo-1-2048x1651.png`, `matplotlib.png`, `plotly.png`, `seaborn.png`, `statistics.png`
* **Infraestrutura**

  * `Dockerfile`, `docker-compose.yml`, `requirements.txt`, `pyproject.toml`, `.env(.example)`


---

## 🛠️ Abrir e rodar o projeto

Para iniciar o projeto localmente, siga os passos abaixo:

1. **Pré-requisitos**

   * Python 3.11+
   * PostgreSQL
   * (Opcional) Docker/Docker Compose
   * (Opcional) Java 17 para PySpark (no Docker já vem instalado)

2. **Clone o Repositório**

```bash
git clone <URL_DO_REPOSITORIO>
cd moura-stack-training
```

3. **Configuração do ambiente**

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edite o `.env`:

* `DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/dbname`
* `ETL_SOURCE=csv` (ou `postgres`)
* `POWER_BI_EMBED_URL=` (opcional)

> **Dica**: se você **não** possui `sql/02_reset_sales.sql`, defina `DB_AUTO_INIT=false` para evitar tentativa automática de *reset*.

4. **Rodar o Banco (schema inicial)**

```bash
psql "postgresql://user:pass@host:5432/dbname" -f sql/01_init.sql
```

5. **Iniciar o Backend**

```bash
uvicorn app.backend.main:app --reload --port 8000
# Docs: http://localhost:8000/docs
# Dashboard: http://localhost:8000/
```

6. **Dashboard Jinja**
   A página principal `/` já carrega KPIs, tabela e filtros.

> **Atenção**: se os filtros do front apontarem para `/metrics/*`, troque para `/api/*` (ou adicione os *routers* equivalentes).

7. **ETL & Exportações (exemplos)**

```bash
curl -X POST http://localhost:8000/etl/run
curl -X POST http://localhost:8000/gold/export
curl -X POST http://localhost:8000/export/excel
```

8. **Rodar Spark (opcional)**

```bash
python scripts/generate_charts/pyspark_agg.py
```

---

## 🌐 Deploy

* **Docker (local)**

```bash
docker compose up --build
```

* **Nuvem**

  * **API**: publique a imagem Docker (Railway, Render, Fly.io, AWS ECS, etc.).
  * **Banco**: use PostgreSQL gerenciado (RDS/CloudSQL/Azure).
  * **dbt**: aponte para o Postgres da nuvem e rode `dbt run`.
  * **Power BI**: configure `POWER_BI_EMBED_URL`.
