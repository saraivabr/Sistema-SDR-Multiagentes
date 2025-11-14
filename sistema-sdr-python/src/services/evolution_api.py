"""
Cliente para Evolution API - envio de mensagens WhatsApp.
"""

from typing import Dict, List

import httpx

from src.config import get_settings

settings = get_settings()


class EvolutionAPIClient:
    """Cliente para interagir com Evolution API."""

    def __init__(self) -> None:
        """Inicializa cliente HTTP."""
        self.base_url = settings.EVOLUTION_API_URL.rstrip("/")
        self.instance = settings.EVOLUTION_INSTANCE
        self.api_key = settings.EVOLUTION_API_KEY

        self.headers = {
            "Content-Type": "application/json",
            "apikey": self.api_key,
        }

    async def send_text_message(self, phone: str, text: str) -> Dict:
        """
        Envia mensagem de texto.

        Args:
            phone: Número do telefone (com código do país)
            text: Texto da mensagem

        Returns:
            Resposta da API
        """
        import structlog

        logger = structlog.get_logger()

        url = f"{self.base_url}/message/sendText/{self.instance}"

        payload = {
            "number": phone,
            "text": text,
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload, headers=self.headers, timeout=30.0)
                response.raise_for_status()

                logger.info("message_sent", phone=phone, status=response.status_code)
                return response.json()

            except httpx.HTTPError as e:
                logger.error("message_send_failed", exc_info=e, phone=phone)
                raise

    async def send_media_message(self, phone: str, media_url: str, caption: str | None = None) -> Dict:
        """
        Envia mensagem com mídia (imagem, vídeo, documento).

        Args:
            phone: Número do telefone
            media_url: URL da mídia
            caption: Legenda opcional

        Returns:
            Resposta da API
        """
        import structlog

        logger = structlog.get_logger()

        url = f"{self.base_url}/message/sendMedia/{self.instance}"

        payload = {
            "number": phone,
            "mediatype": "image",  # Detectar automaticamente ou passar como parâmetro
            "media": media_url,
        }

        if caption:
            payload["caption"] = caption

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload, headers=self.headers, timeout=30.0)
                response.raise_for_status()

                logger.info("media_sent", phone=phone, media_url=media_url)
                return response.json()

            except httpx.HTTPError as e:
                logger.error("media_send_failed", exc_info=e, phone=phone, media_url=media_url)
                raise

    async def send_multiple_media(self, phone: str, media_urls: List[str]) -> List[Dict]:
        """
        Envia múltiplas mídias em sequência.

        Args:
            phone: Número do telefone
            media_urls: Lista de URLs de mídia

        Returns:
            Lista de respostas da API
        """
        responses = []
        for media_url in media_urls[:5]:  # Limite de 5 mídias
            response = await self.send_media_message(phone, media_url)
            responses.append(response)
        return responses

    async def get_instance_status(self) -> Dict:
        """
        Verifica status da instância.

        Returns:
            Status da conexão WhatsApp
        """
        url = f"{self.base_url}/instance/connectionState/{self.instance}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers, timeout=10.0)
            response.raise_for_status()
            return response.json()
