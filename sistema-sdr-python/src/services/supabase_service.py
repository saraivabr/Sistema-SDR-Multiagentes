"""
Serviço de integração com Supabase para Vector Store (RAG).
"""

from typing import Any, Dict, List

from supabase import Client, create_client

from src.config import get_settings

settings = get_settings()


class SupabaseService:
    """Serviço para busca vetorial no Supabase."""

    def __init__(self) -> None:
        """Inicializa cliente Supabase."""
        self.client: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        self.table_loteamentos = settings.SUPABASE_TABLE_LOTEAMENTOS
        self.table_construtora = settings.SUPABASE_TABLE_CONSTRUTORA

    async def search_loteamentos(
        self, query_embedding: List[float], top_k: int | None = None, loteamento: str | None = None
    ) -> List[Dict[str, Any]]:
        """
        Busca documentos sobre loteamentos usando similaridade vetorial.

        Args:
            query_embedding: Vetor de embedding da query
            top_k: Número de resultados (default: configuração)
            loteamento: Filtrar por loteamento específico (opcional)

        Returns:
            Lista de documentos relevantes com metadata
        """
        top_k = top_k or settings.RAG_TOP_K_LOTEAMENTOS

        # Busca vetorial
        response = (
            self.client.rpc(
                "match_documents",
                {
                    "query_embedding": query_embedding,
                    "match_threshold": 0.7,
                    "match_count": top_k,
                    "table_name": self.table_loteamentos,
                },
            )
            .execute()
        )

        results = response.data

        # Filtrar por loteamento se especificado
        if loteamento and results:
            results = [
                doc
                for doc in results
                if doc.get("metadata", {}).get("loteamento", "").lower() == loteamento.lower()
            ]

        return results

    async def search_construtora(
        self, query_embedding: List[float], top_k: int | None = None
    ) -> List[Dict[str, Any]]:
        """
        Busca documentos sobre construção usando similaridade vetorial.

        Args:
            query_embedding: Vetor de embedding da query
            top_k: Número de resultados (default: configuração)

        Returns:
            Lista de documentos relevantes com metadata
        """
        top_k = top_k or settings.RAG_TOP_K_CONSTRUTORA

        # Busca vetorial
        response = (
            self.client.rpc(
                "match_documents",
                {
                    "query_embedding": query_embedding,
                    "match_threshold": 0.7,
                    "match_count": top_k,
                    "table_name": self.table_construtora,
                },
            )
            .execute()
        )

        return response.data

    async def upsert_documents(
        self, documents: List[Dict[str, Any]], table: str = "loteamentos"
    ) -> None:
        """
        Insere ou atualiza documentos no vector store.

        Args:
            documents: Lista de documentos com content, metadata e embedding
            table: Tabela de destino (loteamentos ou construtora)
        """
        table_name = self.table_loteamentos if table == "loteamentos" else self.table_construtora

        response = self.client.table(table_name).upsert(documents).execute()
        return response.data
