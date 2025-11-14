"""
Classe base para todos os agentes do sistema.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import get_settings
from src.db.models import ChatMessage
from src.services.openai_service import OpenAIService

settings = get_settings()
logger = structlog.get_logger()


class BaseAgent(ABC):
    """Classe base abstrata para agentes."""

    def __init__(self, name: str, db: AsyncSession):
        self.name = name
        self.db = db
        self.openai_service = OpenAIService()

    @abstractmethod
    def get_system_prompt(self) -> str:
        """
        Retorna o prompt de sistema do agente.
        Deve ser implementado por cada agente específico.
        """
        pass

    @abstractmethod
    def get_tools(self) -> List[Dict[str, Any]]:
        """
        Retorna lista de tools disponíveis para o agente.
        Formato OpenAI function calling.
        """
        pass

    async def get_chat_history(
        self, session_id: str, limit: int = 10
    ) -> List[Dict[str, str]]:
        """
        Recupera histórico de chat da sessão.

        Args:
            session_id: ID da sessão (telefone)
            limit: Número máximo de mensagens

        Returns:
            Lista de mensagens no formato OpenAI
        """
        query = (
            select(ChatMessage)
            .where(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.timestamp.desc())
            .limit(limit)
        )

        result = await self.db.execute(query)
        messages = result.scalars().all()

        # Converter para formato OpenAI e inverter ordem
        history = [{"role": msg.role, "content": msg.content} for msg in reversed(messages)]

        return history

    async def save_message(
        self, session_id: str, role: str, content: str, metadata: Dict[str, Any] | None = None
    ) -> None:
        """
        Salva mensagem no histórico.

        Args:
            session_id: ID da sessão
            role: Role da mensagem (user/assistant/system/function)
            content: Conteúdo da mensagem
            metadata: Metadata adicional (opcional)
        """
        import json

        message = ChatMessage(
            session_id=session_id,
            role=role,
            content=content,
            agent_name=self.name,
            metadata=json.dumps(metadata) if metadata else None,
        )

        self.db.add(message)
        await self.db.commit()

    async def execute(self, session_id: str, user_message: str) -> str:
        """
        Executa o agente para processar mensagem do usuário.

        Args:
            session_id: ID da sessão
            user_message: Mensagem do usuário

        Returns:
            Resposta do agente
        """
        logger.info("agent_execution_start", agent=self.name, session_id=session_id)

        try:
            # Salvar mensagem do usuário
            await self.save_message(session_id, role="user", content=user_message)

            # Carregar histórico
            history = await self.get_chat_history(session_id, limit=10)

            # Construir mensagens para OpenAI
            messages = [
                {"role": "system", "content": self.get_system_prompt()},
                *history,
            ]

            # Chamar OpenAI
            tools = self.get_tools()
            response = await self.openai_service.chat_completion(
                messages=messages, tools=tools if tools else None
            )

            # Processar resposta
            assistant_message = response.choices[0].message

            # Se há tool calls, processar
            if assistant_message.tool_calls:
                tool_response = await self._handle_tool_calls(
                    session_id, assistant_message.tool_calls
                )
                # Salvar resposta do agente
                await self.save_message(
                    session_id,
                    role="assistant",
                    content=tool_response,
                    metadata={"tool_calls": len(assistant_message.tool_calls)},
                )
                return tool_response

            # Resposta de texto normal
            content = assistant_message.content or ""
            await self.save_message(session_id, role="assistant", content=content)

            logger.info(
                "agent_execution_complete", agent=self.name, response_length=len(content)
            )

            return content

        except Exception as e:
            logger.error("agent_execution_error", exc_info=e, agent=self.name, session_id=session_id)
            raise

    async def _handle_tool_calls(self, session_id: str, tool_calls: List[Any]) -> str:
        """
        Processa chamadas de ferramentas.

        Args:
            session_id: ID da sessão
            tool_calls: Lista de tool calls do OpenAI

        Returns:
            Resultado agregado das ferramentas
        """
        # Implementação básica - deve ser estendida por agentes específicos
        results = []

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            logger.info("tool_call", function=function_name, session_id=session_id)

            # Aqui você chamaria a ferramenta real
            # Por enquanto, log apenas
            results.append(f"Tool {function_name} executed")

        return " ".join(results)
