"""
Endpoints de health check e status da aplicação.
"""

from typing import Dict

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import get_settings
from src.db.session import get_db

router = APIRouter()
settings = get_settings()


@router.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check básico.
    Retorna status OK se aplicação está rodando.
    """
    return {
        "status": "ok",
        "service": "Sistema SDR Multi-Agentes",
        "version": "1.0.0",
        "environment": settings.API_ENV,
    }


@router.get("/health/detailed")
async def detailed_health_check(db: AsyncSession = Depends(get_db)) -> Dict[str, any]:
    """
    Health check detalhado com verificação de dependências.
    Verifica conexões com database, APIs externas, etc.
    """
    import structlog

    logger = structlog.get_logger()

    health_status = {
        "status": "ok",
        "service": "Sistema SDR Multi-Agentes",
        "version": "1.0.0",
        "environment": settings.API_ENV,
        "checks": {},
    }

    # Check PostgreSQL
    try:
        result = await db.execute(text("SELECT 1"))
        await result.fetchone()
        health_status["checks"]["database"] = "ok"
    except Exception as e:
        logger.error("database_health_check_failed", exc_info=e)
        health_status["checks"]["database"] = "error"
        health_status["status"] = "degraded"

    # Check OpenAI (verificar se API key está configurada)
    if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY.startswith("sk-"):
        health_status["checks"]["openai"] = "configured"
    else:
        health_status["checks"]["openai"] = "not_configured"
        health_status["status"] = "degraded"

    # Check Supabase (verificar se está configurado)
    if settings.SUPABASE_URL and settings.SUPABASE_KEY:
        health_status["checks"]["supabase"] = "configured"
    else:
        health_status["checks"]["supabase"] = "not_configured"
        health_status["status"] = "degraded"

    # Check Evolution API (verificar se está configurado)
    if settings.EVOLUTION_API_URL and settings.EVOLUTION_API_KEY:
        health_status["checks"]["evolution_api"] = "configured"
    else:
        health_status["checks"]["evolution_api"] = "not_configured"
        health_status["status"] = "degraded"

    return health_status
