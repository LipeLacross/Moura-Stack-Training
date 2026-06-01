# Power Automate - Fluxo de Aprovação de Ordens de Produção

## Visão Geral
Fluxo que dispara quando uma ordem de produção ultrapassa R$ 50.000 e precisa de aprovação do gestor.

## Gatilho (Trigger)
- **Tipo:** Quando um novo item é criado (SQL)
- **Fonte:** `producao.ordens_producao`
- **Condição:** `quantidade_planejada * preco_custo > 50000`

## Passos do Fluxo

### 1. Obter Detalhes da Ordem
```sql
SELECT op.id_ordem, p.nome, op.quantidade_planejada, p.preco_custo,
       (op.quantidade_planejada * p.preco_custo) as valor_total
FROM producao.ordens_producao op
JOIN producao.produtos p ON op.id_produto = p.id_produto
WHERE op.id_ordem = @{triggerBody()?['id_ordem']}
```

### 2. Calcular Valor
- **Operação:** Multiplicar quantidade planejada por preço de custo
- **Resultado:** Armazenar em variável `valorOrdem`

### 3. Condicional (Valor > 50.000?)
- **Se SIM:** Iniciar aprovação
- **Se NÃO:** Atualizar status para "aprovado automaticamente"

### 4. Solicitar Aprovação
- **Tipo:** Aprovação de conteúdo
- **Atribuído a:** [Gestor de Produção]
- **Detalhes:**
  - Título: `Ordem #{id_ordem} - {produto}`
  - Valor: `R$ {valorTotal}`
  - Link: `http://localhost:8000/api/processes/{id_ordem}`

### 5. Aguardar Resposta
- **Aprovado:** Atualizar status para "aprovado" e notificar solicitante
- **Rejeitado:** Atualizar status para "rejeitado" e notificar com justificativa

### 6. Notificação por E-mail
- **Template:** `ordem_aprovada.html` ou `ordem_rejeitada.html`
- **Destinatário:** Solicitante da ordem

## JSON do Fluxo (Export)
```json
{
  "name": "Aprovacao Ordem Producao",
  "trigger": {
    "type": "SqlServerTrigger",
    "table": "ordens_producao",
    "operation": "Create"
  },
  "actions": {
    "calcular_valor": { "type": "VariableOperation" },
    "verificar_limiar": { "type": "Condition" },
    "solicitar_aprovacao": { "type": "Approval" }
  }
}
```
