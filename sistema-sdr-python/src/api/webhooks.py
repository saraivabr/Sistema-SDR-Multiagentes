"""
Endpoints de webhook para receber mensagens da Evolution API.
"""

from typing import Any, Dict

from fastapi import APIRouter, BackgroundTasks, Depends, Header, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import get_settings
from src.core.message_processor import MessageProcessor
from src.db.session import get_db

router = APIRouter()
settings = get_settings()


class WhatsAppMessage(BaseModel):
    """Schema para mensagem recebida do WhatsApp via Evolution API."""

    key: Dict[str, Any] = Field(..., description="Chave da mensagem")
    pushName: str | None = Field(None, description="Nome do contato")
    message: Dict[str, Any] = Field(..., description="Conteúdo da mensagem")
    messageType: str = Field(..., description="Tipo da mensagem")
    messageTimestamp: int = Field(..., description="Timestamp da mensagem")
    instanceId: str | None = Field(None, description="ID da instância")


class EvolutionWebhook(BaseModel):
    """Schema para webhook completo da Evolution API."""

    event: str = Field(..., description="Tipo do evento")
    instance: str = Field(..., description="Nome da instância")
    data: WhatsAppMessage = Field(..., description="Dados da mensagem")


@router.post("/evolution")
async def evolution_webhook(
    webhook_data: EvolutionWebhook,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    authorization: str | None = Header(None),
) -> Dict[str, str]:
    """
    Endpoint webhook para receber mensagens da Evolution API.

    Fluxo:
    1. Valida autenticação
    2. Extrai dados da mensagem
    3. Enfileira processamento em background
    4. Retorna resposta rápida (ACK)
    """
    import structlog

    logger = structlog.get_logger()

    # Validar autenticação (Bearer token)
    if settings.API_ENV == "production":
        if not authorization or not authorization.startswith("Bearer "):
            logger.warning("webhook_unauthorized_access", headers={"authorization": authorization})
            raise HTTPException(status_code=401, detail="Unauthorized")

        token = authorization.replace("Bearer ", "")
        if token != settings.EVOLUTION_API_KEY:
            logger.warning("webhook_invalid_token")
            raise HTTPException(status_code=401, detail="Invalid token")

    # Log recebimento
    logger.info(
        "webhook_received",
        event=webhook_data.event,
        instance=webhook_data.instance,
        message_type=webhook_data.data.messageType,
    )

    # Processar apenas eventos de mensagens
    if webhook_data.event != "messages.upsert":
        logger.debug("webhook_event_ignored", event=webhook_data.event)
        return {"status": "ignored", "reason": "event_type_not_supported"}

    # Extrair session_id (número de telefone)
    try:
        session_id = webhook_data.data.key.get("remoteJid", "").split("@")[0]
        if not session_id:
            raise ValueError("Session ID not found")
    except Exception as e:
        logger.error("webhook_invalid_session_id", exc_info=e, key=webhook_data.data.key)
        raise HTTPException(status_code=400, detail="Invalid session ID")

    # Enfileirar processamento em background
    message_processor = MessageProcessor(db=db)
    background_tasks.add_task(
        message_processor.process_webhook_message,
        session_id=session_id,
        webhook_data=webhook_data.dict(),
    )

    # Retornar ACK rápido
    return {"status": "accepted", "session_id": session_id}


@router.get("/test")
async def test_webhook() -> Dict[str, str]:
    """Endpoint de teste para verificar se webhook está acessível."""
    return {
        "status": "ok",
        "message": "Webhook endpoint is accessible",
        "instance": settings.EVOLUTION_INSTANCE,
    }
