"""
Modelos SQLAlchemy para o banco de dados PostgreSQL.
Define as tabelas: leads e chat_memory.
"""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Classe base para todos os modelos."""

    pass


class Lead(Base):
    """
    Modelo para tabela de leads.
    Armazena informações de contatos e seu status de qualificação.
    """

    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telefone: Mapped[str] = mapped_column(
        String(20), unique=True, nullable=False, index=True, comment="Telefone do lead (sessionId)"
    )
    nome: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="Nome do lead")
    interesse: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        index=True,
        comment="Interesse: Loteamentos, Construtora, etc.",
    )
    qualificado: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False, index=True, comment="Lead qualificado para especialista"
    )
    notas: Mapped[Optional[str]] = mapped_column(
        String(250), nullable=True, comment="Anotações sobre o lead (máx 250 chars)"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<Lead(telefone={self.telefone}, nome={self.nome}, interesse={self.interesse})>"


class ChatMessage(Base):
    """
    Modelo para histórico de mensagens (chat memory).
    Armazena todas as mensagens trocadas com os usuários.
    """

    __tablename__ = "chat_memory"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    session_id: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True, comment="ID da sessão (telefone)"
    )
    role: Mapped[str] = mapped_column(
        String(20), nullable=False, comment="Role: user, assistant, system, function"
    )
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="Conteúdo da mensagem")
    agent_name: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, comment="Nome do agente que gerou a mensagem"
    )
    metadata: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, comment="Metadata adicional em JSON"
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )

    def __repr__(self) -> str:
        return f"<ChatMessage(session_id={self.session_id}, role={self.role}, timestamp={self.timestamp})>"
