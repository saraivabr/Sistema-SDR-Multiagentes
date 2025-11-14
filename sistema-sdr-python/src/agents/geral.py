"""
Agente Geral - Atendimento inicial e triagem.
"""

from typing import Any, Dict, List

from sqlalchemy.ext.asyncio import AsyncSession

from src.agents.base import BaseAgent
from src.config import get_settings
from src.prompts.geral import AGENTE_GERAL_PROMPT

settings = get_settings()


class AgenteGeral(BaseAgent):
    """
    Agente Geral para atendimento inicial.

    Responsabilidades:
    - Saudação inicial
    - Coleta de nome
    - Identificação de necessidades
    - Direcionamento para canais apropriados
    """

    def __init__(self, db: AsyncSession):
        super().__init__(name="agente_geral", db=db)

    def get_system_prompt(self) -> str:
        """Retorna prompt do Agente Geral."""
        return AGENTE_GERAL_PROMPT

    def get_tools(self) -> List[Dict[str, Any]]:
        """Tools disponíveis para o Agente Geral."""
        return [
            {
                "type": "function",
                "function": {
                    "name": "cadastro_lead",
                    "description": "Salva o nome do lead no banco de dados quando ele informar pela primeira vez",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "nome": {
                                "type": "string",
                                "description": "Nome do lead",
                            }
                        },
                        "required": ["nome"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "anotacao_lead",
                    "description": "Adiciona anotações sobre a conversa para o vendedor (máx 250 chars)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "notas": {
                                "type": "string",
                                "description": "Anotações em bullet points, máximo 250 caracteres",
                                "maxLength": 250,
                            }
                        },
                        "required": ["notas"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "think",
                    "description": "Use para pensar e analisar antes de decisões importantes",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "pensamento": {
                                "type": "string",
                                "description": "Sua análise interna da situação",
                            }
                        },
                        "required": ["pensamento"],
                    },
                },
            },
        ]
