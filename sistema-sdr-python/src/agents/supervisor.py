"""
Agente Supervisor - Router inteligente para direcionar mensagens.
"""

from typing import Any, Dict, List

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from src.agents.base import BaseAgent
from src.agents.geral import AgenteGeral
from src.config import get_settings

settings = get_settings()
logger = structlog.get_logger()


class SupervisorAgent(BaseAgent):
    """
    Agente Supervisor que roteia mensagens para agentes especializados.

    Responsabilidades:
    - Analisar contexto da conversa
    - Decidir qual agente deve responder
    - Manter log de decisões
    - Fallback para Agente Geral
    """

    def __init__(self, db: AsyncSession):
        super().__init__(name="supervisor", db=db)

        # Inicializar agentes especializados
        self.agente_geral = AgenteGeral(db=db)
        # TODO: Adicionar outros agentes quando implementados
        # self.agente_loteamentos = AgenteLoteamentos(db=db)
        # self.agente_construtora = AgenteConstrutora(db=db)

    def get_system_prompt(self) -> str:
        """Prompt do supervisor para roteamento."""
        return f"""Você é o Agente Supervisor do sistema de atendimento Le Mans via WhatsApp.

Sua função é analisar a mensagem e o contexto para decidir qual agente deve responder:

1. **Agente Geral** (agente_geral):
   - Primeira mensagem do usuário
   - Saudações iniciais
   - Assuntos gerais
   - Quando não há certeza

2. **Agente Loteamentos** (agente_loteamentos):
   - Interesse em terrenos, lotes
   - Perguntas sobre loteamentos
   - Investimento em terra

3. **Agente Construtora** (agente_construtora):
   - Interesse em construir casa
   - Projetos de construção
   - Orçamentos de obra

IMPORTANTE:
- SEMPRE use a função `think` antes de decidir
- Considere o histórico completo da conversa
- Em caso de dúvida, escolha Agente Geral
- Primeira mensagem SEMPRE vai para Agente Geral

Retorne apenas o nome do agente escolhido: "agente_geral", "agente_loteamentos" ou "agente_construtora"
"""

    def get_tools(self) -> List[Dict[str, Any]]:
        """Tools do supervisor (Think Tool)."""
        return [
            {
                "type": "function",
                "function": {
                    "name": "think",
                    "description": "Use this to think and analyze before making a routing decision",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "analysis": {
                                "type": "string",
                                "description": "Your internal analysis of the conversation and context",
                            },
                            "decision": {
                                "type": "string",
                                "description": "The agent you decided to route to",
                                "enum": ["agente_geral", "agente_loteamentos", "agente_construtora"],
                            },
                        },
                        "required": ["analysis", "decision"],
                    },
                },
            }
        ]

    async def route_and_respond(self, session_id: str, user_message: str) -> str:
        """
        Roteia mensagem para agente apropriado e retorna resposta.

        Args:
            session_id: ID da sessão
            user_message: Mensagem do usuário

        Returns:
            Resposta do agente selecionado
        """
        # Determinar qual agente usar
        selected_agent_name = await self._select_agent(session_id, user_message)

        logger.info(
            "routing_decision",
            session_id=session_id,
            selected_agent=selected_agent_name,
        )

        # Chamar agente selecionado
        agent = self._get_agent(selected_agent_name)
        response = await agent.execute(session_id, user_message)

        return response

    async def _select_agent(self, session_id: str, user_message: str) -> str:
        """
        Analisa contexto e seleciona agente apropriado.

        Args:
            session_id: ID da sessão
            user_message: Mensagem do usuário

        Returns:
            Nome do agente selecionado
        """
        # Carregar histórico
        history = await self.get_chat_history(session_id, limit=5)

        # Se primeira mensagem, sempre Agente Geral
        if not history or len(history) == 0:
            logger.info("first_message_routing_to_geral", session_id=session_id)
            return "agente_geral"

        # TODO: Implementar lógica de roteamento mais sofisticada
        # Por enquanto, usar keywords simples

        message_lower = user_message.lower()

        # Keywords para loteamentos
        loteamentos_keywords = ["terreno", "lote", "loteamento", "terra", "investimento"]
        if any(keyword in message_lower for keyword in loteamentos_keywords):
            return "agente_loteamentos"

        # Keywords para construtora
        construtora_keywords = ["construir", "casa", "obra", "projeto", "construção"]
        if any(keyword in message_lower for keyword in construtora_keywords):
            return "agente_construtora"

        # Default: Agente Geral
        return "agente_geral"

    def _get_agent(self, agent_name: str) -> BaseAgent:
        """
        Retorna instância do agente pelo nome.

        Args:
            agent_name: Nome do agente

        Returns:
            Instância do agente
        """
        agents = {
            "agente_geral": self.agente_geral,
            # "agente_loteamentos": self.agente_loteamentos,
            # "agente_construtora": self.agente_construtora,
        }

        # Fallback para agente geral
        return agents.get(agent_name, self.agente_geral)
