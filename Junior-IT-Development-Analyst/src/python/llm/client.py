from openai import OpenAI
from typing import Optional


class LLMClient:
    def __init__(self, api_key: str, endpoint: str = "https://api.openai.com/v1", model: str = "gpt-4o-mini"):
        self.client = OpenAI(api_key=api_key, base_url=endpoint)
        self.model = model

    def generate(
        self,
        prompt: str,
        system_context: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> dict:
        messages = []
        if system_context:
            messages.append({"role": "system", "content": system_context})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        return {
            "content": response.choices[0].message.content,
            "model": response.model,
            "tokens_used": response.usage.total_tokens if response.usage else 0,
        }

    def generate_structured(
        self,
        prompt: str,
        system_context: Optional[str] = None,
    ) -> str:
        return self.generate(
            prompt=prompt,
            system_context=system_context or "Responda de forma estruturada e concisa.",
            temperature=0.3,
        )["content"]
