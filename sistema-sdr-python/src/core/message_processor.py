"""
Processador de mensagens do WhatsApp.
Classifica, sanitiza e roteia mensagens para o sistema de agentes.
"""

import asyncio
from datetime import datetime, timedelta
from typing import Any, Dict

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from src.agents.supervisor import SupervisorAgent
from src.config import get_settings
from src.services.evolution_api import EvolutionAPIClient

settings = get_settings()
logger = structlog.get_logger()


class MessageBuffer:
    """Buffer de mensagens para agrupar mensagens fragmentadas."""

    def __init__(self, seconds: int = 10):
        self.buffer: Dict[str, list] = {}
        self.timers: Dict[str, asyncio.Task] = {}
        self.buffer_seconds = seconds

    async def add_message(self, session_id: str, message: str, callback) -> None:
        """
        Adiciona mensagem ao buffer e agenda processamento.

        Args:
            session_id: ID da sessão (telefone)
            message: Mensagem recebida
            callback: Função a chamar após buffer expirar
        """
        # Adicionar mensagem ao buffer
        if session_id not in self.buffer:
            self.buffer[session_id] = []
        self.buffer[session_id].append(message)

        # Cancelar timer existente
        if session_id in self.timers:
            self.timers[session_id].cancel()

        # Criar novo timer
        async def process_after_delay():
            await asyncio.sleep(self.buffer_seconds)
            messages = self.buffer.pop(session_id, [])
            combined_message = " ".join(messages).strip()
            if combined_message:
                await callback(session_id, combined_message)
            self.timers.pop(session_id, None)

        self.timers[session_id] = asyncio.create_task(process_after_delay())


# Buffer global
message_buffer = MessageBuffer(seconds=settings.MESSAGE_BUFFER_SECONDS)


class MessageProcessor:
    """Processador principal de mensagens."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.evolution_client = EvolutionAPIClient()
        self.supervisor = SupervisorAgent(db=db)

    async def process_webhook_message(self, session_id: str, webhook_data: Dict[str, Any]) -> None:
        """
        Processa mensagem recebida do webhook.

        Fluxo:
        1. Extrai conteúdo da mensagem
        2. Classifica tipo (texto/áudio/imagem)
        3. Processa mídia se necessário (OCR/transcrição)
        4. Adiciona ao buffer
        """
        try:
            message_data = webhook_data["data"]["message"]
            message_type = webhook_data["data"]["messageType"]

            logger.info(
                "processing_message",
                session_id=session_id,
                message_type=message_type,
            )

            # Extrair texto da mensagem baseado no tipo
            text = await self._extract_text_from_message(message_data, message_type)

            if not text:
                logger.warning("no_text_extracted", session_id=session_id, message_type=message_type)
                return

            # Adicionar ao buffer
            await message_buffer.add_message(session_id, text, self._process_buffered_message)

        except Exception as e:
            logger.error("message_processing_error", exc_info=e, session_id=session_id)

    async def _extract_text_from_message(self, message_data: Dict, message_type: str) -> str:
        """
        Extrai texto da mensagem baseado no tipo.

        Args:
            message_data: Dados da mensagem
            message_type: Tipo da mensagem

        Returns:
            Texto extraído
        """
        # Mensagem de texto
        if message_type in ["conversation", "extendedTextMessage"]:
            return (
                message_data.get("conversation")
                or message_data.get("extendedTextMessage", {}).get("text")
                or ""
            )

        # Áudio (implementar transcrição futuramente)
        elif message_type == "audioMessage":
            # TODO: Implementar transcrição com Whisper
            logger.info("audio_message_received", message="Transcrição não implementada ainda")
            return "[Áudio recebido - transcrição em desenvolvimento]"

        # Imagem/Documento (implementar OCR futuramente)
        elif message_type in ["imageMessage", "documentMessage"]:
            # TODO: Implementar OCR com pytesseract
            logger.info("media_message_received", message_type=message_type)
            return "[Mídia recebida - OCR em desenvolvimento]"

        return ""

    async def _process_buffered_message(self, session_id: str, combined_message: str) -> None:
        """
        Processa mensagem após buffer expirar.
        Envia para o supervisor que roteia para agente apropriado.

        Args:
            session_id: ID da sessão
            combined_message: Mensagem combinada do buffer
        """
        try:
            logger.info(
                "processing_buffered_message",
                session_id=session_id,
                message_length=len(combined_message),
            )

            # Chamar supervisor para processar e responder
            response = await self.supervisor.route_and_respond(
                session_id=session_id, user_message=combined_message
            )

            # Enviar resposta via Evolution API
            await self.evolution_client.send_text_message(phone=session_id, text=response)

            logger.info("response_sent", session_id=session_id, response_length=len(response))

        except Exception as e:
            logger.error("buffered_message_processing_error", exc_info=e, session_id=session_id)
            # Enviar mensagem de erro ao usuário
            await self._send_error_message(session_id)

    async def _send_error_message(self, session_id: str) -> None:
        """Envia mensagem de erro amigável ao usuário."""
        error_msg = (
            f"Desculpe, tive um problema técnico. 😔\n"
            f"Tente novamente em alguns instantes ou entre em contato diretamente pelo "
            f"{settings.LEMANS_IMOVEIS_PHONE}."
        )
        try:
            await self.evolution_client.send_text_message(phone=session_id, text=error_msg)
        except Exception as e:
            logger.error("error_message_send_failed", exc_info=e, session_id=session_id)
