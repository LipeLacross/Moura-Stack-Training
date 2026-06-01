# Especificação Técnica - Sistema de Automação Moura TI

## 1. Arquitetura

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Frontend   │────>│   FastAPI    │────>│  PostgreSQL  │
│  (JS/HTML)   │     │   (Python)   │     │              │
└──────────────┘     └──────┬───────┘     └──────────────┘
                            │
                    ┌───────┴────────┐
                    │   ML Models    │
                    │  (scikit-learn)│
                    └───────┬────────┘
                            │
                    ┌───────┴────────┐
                    │  LLM / OpenAI  │
                    │  (IA Generativa)│
                    └────────────────┘
```

## 2. Stack Tecnológico

| Componente | Tecnologia | Versão |
|------------|-----------|--------|
| Linguagem Principal | Python | 3.11+ |
| API | FastAPI | 0.115+ |
| ORM | SQLAlchemy | 2.0+ |
| Banco | PostgreSQL | 15+ |
| ML | scikit-learn | 1.6+ |
| LLM | OpenAI API | 1.56+ |
| Dashboard | Streamlit / Plotly | 1.40+ / 5.25+ |
| Frontend | JavaScript + Chart.js | ES6 |
| Backend Alternativo | C# (.NET 8) | 8.0 |
| ETL | Prefect / pandas | 3.0+ |
| Processos | BPMN 2.0 | - |

## 3. Endpoints da API

### 3.1 Processos
```
GET    /api/processes/       - Listar processos
POST   /api/processes/       - Criar processo
GET    /api/processes/{id}   - Obter processo
PUT    /api/processes/{id}   - Atualizar processo
DELETE /api/processes/{id}   - Excluir processo
```

### 3.2 Machine Learning
```
POST /api/ml/predict    - Predição (classifier/regressor/cluster)
POST /api/ml/train      - Treinar modelos
```

### 3.3 LLM / IA Generativa
```
POST /api/llm/generate          - Gerar texto
POST /api/llm/analyze-sentiment - Análise de sentimento
POST /api/llm/generate-report   - Relatório técnico
```

### 3.4 Integração
```
POST /api/integration/sync      - Sincronizar sistemas
GET  /api/integration/sync/history - Histórico de sincronização
GET  /api/integration/systems   - Listar sistemas disponíveis
```

## 4. Estrutura do Banco de Dados

### Schema: producao
- `produtos` - Catálogo de produtos
- `ordens_producao` - Ordens de produção
- `log_operacoes` - Auditoria

### Schema: vendas
- `vendas` - Registro de vendas
- `resumo_diario` - Consolidação diária

### Schema: manutencao
- `manutencoes` - Registro de manutenções

### Schema: analytics (Views)
- `vw_performance_mensal`
- `vw_ranking_produtos`
- `vw_saude_maquinas`
- `vw_funil_vendas`
- `vw_previsao_demanda`

## 5. Modelos de Machine Learning

### Classificador (RandomForest)
- **Features:** temperatura, vibração, pressão, horas de operação, carga
- **Target:** risco de falha (0 ou 1)
- **Métrica:** accuracy, precision, recall, f1

### Regressor (RandomForest)
- **Features:** temperatura ambiente, umidade, velocidade produção, qualidade insumo
- **Target:** eficiência (%)
- **Métrica:** RMSE, MAE, R²

### Clusterização (KMeans)
- **Features:** consumo energia, horas operação, temperatura média
- **Clusters:** 3 (por padrão)
- **Métrica:** silhouette score

## 6. Integração com LLM

- **Provedor:** OpenAI / Azure OpenAI
- **Modelo:** gpt-4o-mini (default)
- **Casos de Uso:**
  - Geração de relatórios executivos
  - Documentação de processos
  - Guias de treinamento
  - Análise de sentimento

## 7. ETL Pipeline

1. **Extract:** Leitura de CSV/JSON/Parquet do diretório `data/sample/`
2. **Transform:** Limpeza, fill NA, rename columns, type casting
3. **Load:** Export para Parquet (camada Gold)

## 8. Testes

```bash
# Python
pytest tests/ -v --cov=src.python

# SQL (manual - requer banco PostgreSQL)
psql -f tests/test_sql.sql
```

## 9. Como Executar

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Configurar .env
cp .env.example .env

# 3. API
uvicorn src.python.api.main:app --reload --port 8000

# 4. Dashboard Streamlit
streamlit run src/python/dashboard/app.py

# 5. Frontend JS
cd src/javascript && npx http-server src -p 3000

# 6. .NET API
cd src/dotnet && dotnet run --project ProcessAutomation.Api
```
