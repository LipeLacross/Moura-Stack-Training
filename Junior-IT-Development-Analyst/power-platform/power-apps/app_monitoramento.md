# Power Apps - App de Monitoramento de Produção

## Visão Geral
Aplicativo mobile para supervisores acompanharem a produção em tempo real.

## Telas

### Tela 1: Login
- Campo: Matrícula
- Campo: Senha (conectado ao Azure AD)
- Botão: Entrar

### Tela 2: Dashboard (Home)
- Galeria: Últimas ordens de produção
- Rótulo: Eficiência do dia
- Ícone: Alerta de manutenção (se houver)
- Botão: Nova Ordem

### Tela 3: Detalhes da Ordem
- Exibir: Produto, quantidade, status, datas
- Botão: Atualizar Status
- Botão: Reportar Problema

### Tela 4: Manutenção
- Galeria: Manutenções agendadas
- Formulário: Registrar nova manutenção
- Indicador: Máquinas em alerta

### Tela 5: Relatórios
- Dropdown: Selecionar período
- Botão: Gerar Relatório (chama API LLM)
- Visualizar: Relatório gerado

## Conexões
- **SQL Server:** `producao.ordens_producao`
- **Power Automate:** Fluxo de aprovação
- **API Custom:** `POST /api/llm/generate-report`

## Fórmulas PowerFX

### Eficiência do Dia
```powerfx
Sum(
    Filter(ordens_producao, data_inicio = Today()),
    quantidade_produzida
) / Sum(
    Filter(ordens_producao, data_inicio = Today()),
    quantidade_planejada
)
```

### Alertas de Manutenção
```powerfx
If(
    CountRows(Filter(manutencoes, tipo = "corretiva" And status = "pendente")) > 0,
    "ATENÇÃO: Manutenção corretiva pendente!",
    "Operação normal"
)
```
