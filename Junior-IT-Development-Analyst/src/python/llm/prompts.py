from typing import Optional


class SentimentAnalyzer:
    def __init__(self, llm_client: Optional[any] = None):
        self.llm = llm_client

    def analyze(self, text: str) -> dict:
        prompt = f"""
Analise o sentimento do texto abaixo e retorne APENAS um JSON com:
- "sentimento": "positivo", "negativo" ou "neutro"
- "confianca": 0.0 a 1.0
- "palavras_chave": lista das principais palavras

Texto: "{text}"
"""
        if self.llm:
            result = self.llm.generate_structured(prompt)
            import json
            try:
                return json.loads(result)
            except json.JSONDecodeError:
                pass

        return {"sentimento": "neutro", "confianca": 0.5, "palavras_chave": []}

    def analyze_batch(self, texts: list[str]) -> list[dict]:
        return [self.analyze(t) for t in texts]


class PromptTemplates:
    @staticmethod
    def technical_report(data_summary: dict) -> str:
        return f"""
Com base nos seguintes indicadores, gere um relatório técnico executivo:

Indicadores:
- Período: {data_summary.get('periodo', 'N/A')}
- Receita Total: R$ {data_summary.get('receita', 0):,.2f}
- Volume Produzido: {data_summary.get('volume', 0):,} unidades
- Eficiência Média: {data_summary.get('eficiencia', 0)}%
- Taxa de Falhas: {data_summary.get('taxa_falhas', 0)}%
- Custo Operacional: R$ {data_summary.get('custo_operacional', 0):,.2f}

Estrutura do relatório:
1. Resumo Executivo (3 linhas)
2. Análise de Desempenho (tópicos)
3. Pontos de Atenção
4. Recomendações (3 ações prioritárias)
"""

    @staticmethod
    def process_documentation(process_name: str, steps: list[str]) -> str:
        steps_text = "\n".join(f"{i+1}. {s}" for i, s in enumerate(steps))
        return f"""
Documente o processo abaixo seguindo o padrão BPMN:

Nome do Processo: {process_name}

Etapas:
{steps_text}

Gere:
- Objetivo do processo
- Ator responsável por cada etapa
- Regras de negócio
- Indicadores de sucesso (KPIs)
- Riscos e mitigação
"""

    @staticmethod
    def user_training(system_name: str, features: list[str]) -> str:
        features_text = "\n- ".join([""] + features)
        return f"""
Crie um guia de treinamento para usuários do sistema "{system_name}".

Funcionalidades:{features_text}

O guia deve incluir:
- Objetivo do treinamento
- Público-alvo
- Passo a passo com prints descritivos
- Dicas de uso
- Erros comuns e como resolver
- FAQ (3 perguntas frequentes)
"""
