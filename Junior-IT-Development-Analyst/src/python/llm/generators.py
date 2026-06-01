from .prompts import PromptTemplates
from typing import Optional


class ReportGenerator:
    def __init__(self, llm_client: Optional[any] = None):
        self.llm = llm_client

    def generate_technical_report(self, data_summary: dict) -> str:
        prompt = PromptTemplates.technical_report(data_summary)
        if self.llm:
            return self.llm.generate_structured(prompt)
        return self._fallback_report(data_summary)

    def generate_process_doc(self, process_name: str, steps: list[str]) -> str:
        prompt = PromptTemplates.process_documentation(process_name, steps)
        if self.llm:
            return self.llm.generate_structured(prompt)
        return self._fallback_process_doc(process_name, steps)

    def generate_user_training(self, system_name: str, features: list[str]) -> str:
        prompt = PromptTemplates.user_training(system_name, features)
        if self.llm:
            return self.llm.generate_structured(prompt)
        return self._fallback_training(system_name, features)

    def _fallback_report(self, data: dict) -> str:
        return f"""
## Relatório Técnico - Período: {data.get('periodo', 'N/A')}

### Resumo Executivo
No período analisado, a operação registrou receita de R$ {data.get('receita', 0):,.2f}
com volume de {data.get('volume', 0):,} unidades produzidas.
A eficiência média foi de {data.get('eficiencia', 0)}%.

### Análise de Desempenho
- Receita: R$ {data.get('receita', 0):,.2f}
- Volume: {data.get('volume', 0):,} unidades
- Eficiência: {data.get('eficiencia', 0)}%
- Taxa de Falhas: {data.get('taxa_falhas', 0)}%

### Recomendações
1. Otimizar processos com maior taxa de falha
2. Revisar custos operacionais
3. Manter monitoramento contínuo
"""

    def _fallback_process_doc(self, name: str, steps: list[str]) -> str:
        steps_text = "\n".join(f"  - {s}" for s in steps)
        return f"""
## Documentação do Processo: {name}

### Objetivo
Automatizar e padronizar o fluxo de {name.lower()}.

### Etapas
{steps_text}

### KPIs
- Tempo médio de execução
- Taxa de conformidade
- Volume processado
"""

    def _fallback_training(self, system_name: str, features: list[str]) -> str:
        features_text = "\n".join(f"  - {f}" for f in features)
        return f"""
## Guia de Treinamento: {system_name}

### Objetivo
Capacitar usuários para utilizar o sistema {system_name}.

### Funcionalidades
{features_text}

### Passo a Passo
1. Acesse o sistema com suas credenciais
2. Navegue pelo menu principal
3. Utilize as funcionalidades conforme sua necessidade
4. Em caso de dúvidas, consulte o FAQ

### FAQ
1. **Como resetar minha senha?** - Entre em contato com o suporte de TI
2. **O sistema está lento?** - Verifique sua conexão de rede
3. **Onde vejo meus relatórios?** - No menu "Relatórios" do sistema
"""
