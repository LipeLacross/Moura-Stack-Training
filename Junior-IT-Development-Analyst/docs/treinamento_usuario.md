# Guia de Treinamento - Sistema Moura TI

## Objetivo
Capacitar usuários a utilizar o sistema de automação, dashboards e relatórios.

## Público-alvo
- Analistas de TI
- Analistas de Produção
- Supervisores de Manutenção
- Gestores

---

## Módulo 1: Acessando o Sistema

### 1.1 API (Analistas de TI)
```bash
# Iniciar servidor
uvicorn src.python.api.main:app --reload --port 8000

# Acessar documentação interativa
http://localhost:8000/docs
```

### 1.2 Dashboard Streamlit
```bash
streamlit run src/python/dashboard/app.py
```
Acessar: `http://localhost:8501`

### 1.3 Frontend Web
```bash
cd src/javascript
npx http-server src -p 3000
```
Acessar: `http://localhost:3000`

---

## Módulo 2: Dashboard de Produção

**Tela:** Streamlit Dashboard

### KPIs Principais
- **Receita Total:** Soma de todas as vendas no período
- **Unidades Produzidas:** Volume total fabricado
- **Eficiência Média:** % médio de aproveitamento

### Abas Disponíveis
1. **Série Temporal:** Gráfico de receita e quantidade ao longo do tempo
2. **Distribuição:** Volume por produto e receita por região
3. **Machine Learning:** Previsão de eficiência com parâmetros ajustáveis
4. **Relatório IA:** Geração automática de relatório executivo

---

## Módulo 3: API - Automação de Processos

### Criar Processo
```bash
curl -X POST http://localhost:8000/api/processes/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Processo Teste", "description": "Teste de criacao"}'
```

### Listar Processos
```bash
curl http://localhost:8000/api/processes/
```

### Sincronizar Sistemas
```bash
curl -X POST http://localhost:8000/api/integration/sync \
  -H "Content-Type: application/json" \
  -d '{"source_system": "sap", "target_system": "powerbi", "payload": {"items": [{"id": 1}]}}'
```

---

## Módulo 4: Machine Learning

### Prever Risco de Falha
1. Acesse o dashboard Streamlit
2. Vá até a aba "Machine Learning"
3. Ajuste os parâmetros (temperatura, umidade, etc.)
4. Clique em "Prever Eficiência"
5. Veja o resultado e a importância de cada feature

### Treinar Modelos
Via API:
```bash
curl -X POST http://localhost:8000/api/ml/train
```

---

## Módulo 5: Relatórios com IA

### Gerar Relatório Executivo
1. No dashboard Streamlit, aba "Relatório IA"
2. Clique em "Gerar Relatório"
3. O sistema consolida KPIs e gera análise textual
4. Relatório inclui: resumo, análise, recomendações

---

## Erros Comuns e Soluções

| Erro | Causa | Solução |
|------|-------|---------|
| API não responde | Servidor não iniciado | Execute `uvicorn src.python.api.main:app --reload` |
| Erro de conexão BD | PostgreSQL desligado | Inicie o PostgreSQL |
| Modelo não treinado | Primeira execução | Execute treinamento via `/api/ml/train` |
| LLM sem resposta | Chave API não configurada | Configure `LLM_API_KEY` no `.env` |

## FAQ

**P: Como resetar minha senha?**  
R: O sistema atual não possui autenticação. Implementação futura com JWT.

**P: O dashboard está lento?**  
R: Verifique sua conexão de rede. Dados locais são processados em memória.

**P: Como adicionar novos dados?**  
R: Coloque arquivos CSV no diretório `data/sample/` e execute o ETL.

**P: Onde vejo o log de operações?**  
R: Endpoint `GET /api/integration/sync/history` ou tabela `producao.log_operacoes`.
