"""
Configurações da aplicação usando Pydantic Settings.
Todas as configurações são carregadas de variáveis de ambiente (.env).
"""

from functools import lru_cache
from typing import Literal

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações principais da aplicação."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True)

    # API Configuration
    API_HOST: str = Field(default="0.0.0.0", description="Host da API")
    API_PORT: int = Field(default=8000, description="Porta da API")
    API_ENV: Literal["development", "staging", "production"] = Field(default="development")
    DEBUG: bool = Field(default=False, description="Modo debug")

    # OpenAI
    OPENAI_API_KEY: str = Field(..., description="Chave da API OpenAI")
    OPENAI_MODEL: str = Field(default="gpt-4-turbo-preview", description="Modelo OpenAI")
    OPENAI_TEMPERATURE: float = Field(default=0.7, description="Temperature para geração")
    OPENAI_MAX_TOKENS: int = Field(default=1000, description="Máximo de tokens no contexto")

    # PostgreSQL
    DATABASE_URL: PostgresDsn = Field(..., description="URL de conexão PostgreSQL")
    DATABASE_POOL_SIZE: int = Field(default=10, description="Tamanho do pool de conexões")
    DATABASE_MAX_OVERFLOW: int = Field(default=20, description="Máximo de conexões extras")

    # Supabase
    SUPABASE_URL: str = Field(..., description="URL do projeto Supabase")
    SUPABASE_KEY: str = Field(..., description="Chave API Supabase")
    SUPABASE_TABLE_LOTEAMENTOS: str = Field(
        default="documents_loteamentos", description="Tabela de documentos loteamentos"
    )
    SUPABASE_TABLE_CONSTRUTORA: str = Field(
        default="documents_construtora", description="Tabela de documentos construtora"
    )

    # Evolution API
    EVOLUTION_API_URL: str = Field(..., description="URL base da Evolution API")
    EVOLUTION_INSTANCE: str = Field(..., description="Nome da instância Evolution")
    EVOLUTION_API_KEY: str = Field(..., description="Chave API Evolution")

    # Redis (Optional)
    REDIS_URL: str = Field(default="redis://localhost:6379/0", description="URL Redis")
    REDIS_ENABLED: bool = Field(default=False, description="Habilitar Redis")

    # Application Settings
    MESSAGE_BUFFER_SECONDS: int = Field(
        default=10, description="Segundos de buffer para agrupar mensagens"
    )
    MAX_CONTEXT_TOKENS: int = Field(default=1000, description="Máximo de tokens no contexto")
    MAX_RESPONSE_LINES: int = Field(default=3, description="Máximo de linhas por resposta")
    RAG_TOP_K_LOTEAMENTOS: int = Field(
        default=5, description="Top K resultados RAG loteamentos"
    )
    RAG_TOP_K_CONSTRUTORA: int = Field(
        default=4, description="Top K resultados RAG construtora"
    )

    # Logging
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(default="INFO")
    LOG_FORMAT: Literal["json", "console"] = Field(default="json")

    # Contact Information
    LEMANS_IMOVEIS_PHONE: str = Field(
        default="19 2533-0370", description="Telefone Le Mans Imóveis"
    )
    COMPANY_NAME: str = Field(
        default="Le Mans Loteamentos e Construtora", description="Nome da empresa"
    )
    AGENT_NAME: str = Field(default="Sara", description="Nome do agente virtual")
    TIMEZONE: str = Field(default="America/Sao_Paulo", description="Timezone")

    # OCR & Media Processing
    TESSERACT_PATH: str = Field(default="/usr/bin/tesseract", description="Path Tesseract")
    FFMPEG_PATH: str = Field(default="/usr/bin/ffmpeg", description="Path FFmpeg")

    @property
    def database_url_str(self) -> str:
        """Retorna DATABASE_URL como string."""
        return str(self.DATABASE_URL)


@lru_cache
def get_settings() -> Settings:
    """
    Retorna instância única das configurações (singleton).
    Usa lru_cache para garantir que Settings seja carregado apenas uma vez.
    """
    return Settings()


# Instância global para import direto
settings = get_settings()
