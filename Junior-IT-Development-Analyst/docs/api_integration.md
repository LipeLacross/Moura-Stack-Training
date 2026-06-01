# Guia de Integração entre Sistemas

## Visão Geral

Este guia documenta como integrar os diferentes sistemas do ecossistema Moura TI.

## 1. Sistemas Disponíveis

| Sistema | Protocolo | Endpoint Base |
|---------|-----------|---------------|
| SAP ERP | RFC / BAPI | Via middleware |
| Power BI | REST API / Embed | `/api/integration/sync` |
| Azure Boards | REST API | `https://dev.azure.com/{org}/{project}/_apis` |
| Banco SQL | ODBC / SQLAlchemy | Direto via connection string |
| APIs Externas | REST / Webhook | Configurável |

## 2. Sincronização via API

### Exemplo: SAP -> Power BI

```bash
curl -X POST http://localhost:8000/api/integration/sync \
  -H "Content-Type: application/json" \
  -d '{
    "source_system": "sap",
    "target_system": "powerbi",
    "payload": {
      "items": [
        {"produto": "Bateria Automotiva", "quantidade": 150, "valor": 37500},
        {"produto": "Bateria Estacionária", "quantidade": 45, "valor": 17100}
      ]
    },
    "action": "sync"
  }'
```

### Resposta Esperada
```json
{
  "status": "success",
  "message": "Sincronização de sap para powerbi concluída",
  "sync_id": "a1b2c3d4e5f6",
  "records_processed": 2
}
```

## 3. Webhooks

Para usar a API como webhook do Power Automate:
```
POST http://localhost:8000/api/integration/sync
Content-Type: application/json
```

## 4. Azure Boards Integration

### Configuração
```bash
AZURE_DEVOPS_ORG=sua-organizacao
AZURE_DEVOPS_PROJECT=seu-projeto
AZURE_DEVOPS_PAT=seu-personal-access-token
```

### Exemplo de Work Item
```json
{
  "source_system": "azure-boards",
  "target_system": "sql-database",
  "payload": {
    "work_items": [
      {"id": 42, "title": "Implementar automação", "state": "Active", "assigned_to": "joao.silva"}
    ]
  },
  "action": "sync"
}
```

## 5. Integração com SAP

A integração com SAP pode ser feita através de:
- **BAPI/RFC:** Usando bibliotecas Python (pyRFC) ou .NET (NCo)
- **IDocs:** Processamento de mensagens EDI
- **SAP Scripts:** Automação via GUI (ver `docs/sap/sap_scripts.md`)

## 6. Log de Sincronização

```bash
# Histórico completo
curl http://localhost:8000/api/integration/sync/history

# Log no banco
SELECT * FROM producao.log_operacoes WHERE operacao = 'sync';
```

## 7. Tratamento de Erros

| Código | Significado | Ação |
|--------|-------------|------|
| 200 | Sucesso | Sincronização concluída |
| 400 | Payload inválido | Verificar JSON |
| 422 | Dados inconsistentes | Validar campos obrigatórios |
| 500 | Erro interno | Verificar logs do servidor |
