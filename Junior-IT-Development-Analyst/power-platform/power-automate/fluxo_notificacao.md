# Power Automate - Notificação de Manutenção Corretiva

## Gatilho
- **Tipo:** Quando um novo item é criado (SQL)
- **Fonte:** `manutencao.manutencoes`
- **Condição:** `tipo = 'corretiva'`

## Ações

### 1. Buscar Responsável
```sql
SELECT tecnico_responsavel, maquina, descricao, custo
FROM manutencao.manutencoes
WHERE id_manutencao = @{triggerBody()?['id_manutencao']}
```

### 2. Notificar Equipe
- **Canal:** Microsoft Teams
- **Mensagem:**
  ```
  🚨 MANUTENÇÃO CORRETIVA
  Máquina: {maquina}
  Técnico: {tecnico}
  Descrição: {descricao}
  Custo Estimado: R$ {custo}
  ```

### 3. Criar Ticket no Azure Boards
- **Tipo:** Issue
- **Título:** `[URGENTE] Manutenção Corretiva - {maquina}`
- **Tags:** `manutencao`, `corretiva`, `urgente`
- **Prioridade:** 2 (Alta)

### 4. Atualizar Dashboard
- Chamar API: `POST /api/integration/sync`
- Payload: dados da manutenção
