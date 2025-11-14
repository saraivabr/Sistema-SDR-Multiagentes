"""
Serviço de integração com OpenAI API.
Wrapper para facilitar uso de GPT-4 e embeddings.
"""

from typing import Any, Dict, List

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion

from src.config import get_settings

settings = get_settings()


class OpenAIService:
    """Serviço para interações com OpenAI API."""

    def __init__(self) -> None:
        """Inicializa cliente OpenAI."""
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        self.temperature = settings.OPENAI_TEMPERATURE
        self.max_tokens = settings.OPENAI_MAX_TOKENS

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float | None = None,
        max_tokens: int | None = None,
        tools: List[Dict[str, Any]] | None = None,
        tool_choice: str | None = None,
    ) -> ChatCompletion:
        """
        Chama API de chat completion do OpenAI.

        Args:
            messages: Lista de mensagens no formato OpenAI
            temperature: Override de temperature (opcional)
            max_tokens: Override de max_tokens (opcional)
            tools: Lista de tools disponíveis para o agente
            tool_choice: Como escolher tools ("auto", "none", ou nome específico)

        Returns:
            Resposta da API OpenAI
        """
        params = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature or self.temperature,
            "max_tokens": max_tokens or self.max_tokens,
        }

        if tools:
            params["tools"] = tools
            params["tool_choice"] = tool_choice or "auto"

        response = await self.client.chat.completions.create(**params)
        return response

    async def create_embedding(self, text: str, model: str = "text-embedding-3-small") -> List[float]:
        """
        Cria embedding para texto.

        Args:
            text: Texto para gerar embedding
            model: Modelo de embedding

        Returns:
            Vetor de embedding
        """
        response = await self.client.embeddings.create(input=text, model=model)
        return response.data[0].embedding

    async def create_embeddings_batch(
        self, texts: List[str], model: str = "text-embedding-3-small"
    ) -> List[List[float]]:
        """
        Cria embeddings para múltiplos textos em batch.

        Args:
            texts: Lista de textos
            model: Modelo de embedding

        Returns:
            Lista de vetores de embedding
        """
        response = await self.client.embeddings.create(input=texts, model=model)
        return [item.embedding for item in response.data]
