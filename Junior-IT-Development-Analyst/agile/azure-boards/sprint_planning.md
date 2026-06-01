# Sprint Planning - Azure Boards

## Sprint Template

### Sprint N: [Nome da Sprint]
- **Período:** DD/MM a DD/MM
- **Objetivo:** [Descrição do objetivo]
- **Time:** [Nomes]

### Planning
| Data | Evento | Participantes |
|------|--------|---------------|
| Segunda | Sprint Planning | PO + Dev Team |
| Diário (15min) | Daily Scrum | Dev Team |
| Sexta (final) | Sprint Review + Retro | PO + Dev Team |

### Definition of Done (DoD)
- Código revisado e aprovado
- Testes unitários passando (>80% cobertura)
- Documentação atualizada
- Pipeline CI/CD verde
- Deploy em homologação

## Exemplo de Daily Scrum

### Formato
1. O que fiz ontem?
2. O que vou fazer hoje?
3. Impedimentos?

### Quadro Kanban
```
┌──────────┬──────────┬──────────┬──────────┐
│ Backlog  │ To Do    │ Doing    │ Done     │
├──────────┼──────────┼──────────┼──────────┤
│ US05     │ US03     │ US04     │ US01     │
│ US06     │          │ BT01     │ US02     │
│ BT03     │          │          │ BT02     │
└──────────┴──────────┴──────────┴──────────┘
```

## Burndown Chart
- **Início:** 20 story points
- **Meta:** 0 no final da sprint
- **Ideal:** Linha reta decrescente
- **Real:** Acompanhamento diário
