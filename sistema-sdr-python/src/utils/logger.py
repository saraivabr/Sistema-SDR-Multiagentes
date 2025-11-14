"""
Configuração de logging estruturado com structlog.
Suporta formato JSON para produção e console para desenvolvimento.
"""

import logging
import sys
from typing import Literal

import structlog


def setup_logging(
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO",
    format_type: Literal["json", "console"] = "console",
) -> None:
    """
    Configura logging estruturado da aplicação.

    Args:
        level: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_type: Formato de saída (json para produção, console para dev)
    """
    # Converter string level para constante do logging
    log_level = getattr(logging, level)

    # Configurar logging padrão do Python
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=log_level,
    )

    # Processar para renderização
    if format_type == "json":
        # JSON para produção (fácil parsing)
        processors = [
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.JSONRenderer(),
        ]
    else:
        # Console colorido para desenvolvimento
        processors = [
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False),
            structlog.dev.ConsoleRenderer(colors=True),
        ]

    # Configurar structlog
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str | None = None) -> structlog.BoundLogger:
    """
    Retorna um logger estruturado.

    Args:
        name: Nome do logger (opcional)

    Returns:
        Logger estruturado do structlog
    """
    return structlog.get_logger(name) if name else structlog.get_logger()
