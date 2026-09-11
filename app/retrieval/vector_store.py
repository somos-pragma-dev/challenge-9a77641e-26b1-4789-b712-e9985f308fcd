import logging
from typing import Any, Optional

import numpy as np
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from pydantic import BaseModel, Field

from app.retrieval.embeddings import EmbeddingsService, create_embeddings_service

logger = logging.getLogger(__name__)


class VectorStoreConfig(BaseModel):
    """Configuración del store vectorial."""

    provider: str = Field(default="faiss", description="Proveedor de almacenamiento vectorial")
    index_name: str = Field(default="normativa_index", description="Nombre del índice")
    persist_directory: Optional[str] = Field(default=None, description="Directorio de persistencia local")
    distance_strategy: str = Field(default="COSINE", description="Estrategia de distancia")
    allow_dangerous_deserialization: bool = Field(default=False)


class VectorStoreResult(BaseModel):
    """Resultado de una búsqueda en el store vectorial."""

    text: str
    metadata: dict[str, Any]
    score: float
    index: int


class VectorStoreService:
    """Servicio para gestión del almacenamiento vectorial y búsquedas semánticas."""

    def __init__(
        self,
        embeddings_service: Optional[EmbeddingsService] = None,
        config: Optional[VectorStoreConfig] = None,
    ) -> None:
        self.config = config or VectorStoreConfig()
        self.embeddings_service = embeddings_service or create_embeddings_service()
        self._vector_store: Optional[FAISS] = None
        self._initialized = False

    @property
    def is_initialized(self) -> bool:
        """Indica si el vector store está inicializado."""
        return self._initialized and self._vector_store is not None

    def create_index(
        self,
        documents: list[dict[str, Any]],
        metadatos: Optional[list[dict[str, Any]]] = None,
    ) -> None:
        """Crea un nuevo índice con los documentos proporcionados."""
        texts = [doc.get("text", doc.get("content", "")) for doc in documents]
        metadatos = metadatos or [doc.get("metadata", {}) for doc in documents]

        if not texts:
            raise ValueError("No se proporcionaron documentos para indexar")

        logger.info("Creando índice con %d documentos", len(texts))

        # Generar embeddings con metadatos
        embedded_docs = self.embeddings_service.embed_with_metadata(texts, metadatos)

        # Crear documentos de LangChain
        langchain_docs = [
            Document(
                page_content=item["text"],
                metadata=item["metadata"],
            )
            for item in embedded_docs
        ]

        # Crear índice FAISS
        embeddings = self.embeddings_service._client
        self._vector_store = FAISS.from_documents(
            documents=langchain_docs,
            embedding=embeddings,
        )

        self._initialized = True
        logger.info("Índice '%s' creado exitosamente", self.config.index_name)

    def add_documents(
        self,
        documents: list[dict[str, Any]],
        metadatos: Optional[list[dict[str, Any]]] = None,
    ) -> None:
        """Agrega documentos a un índice existente."""
        if not self.is_initialized:
            raise RuntimeError("El índice no está inicializado. Use create_index primero.")

        texts = [doc.get("text", doc.get("content", "")) for doc in documents]
        metadatos = metadatos or [doc.get("metadata", {}) for doc in documents]

        embedded_docs = self.embeddings_service.embed_with_metadata(texts, metadatos)

        langchain_docs = [
            Document(
                page_content=item["text"],
                metadata=item["metadata"],
            )
            for item in embedded_docs
        ]

        self._vector_store.add_documents(langchain_docs)
        logger.info("Agregados %d documentos al índice", len(documents))

    def similarity_search(
        self,
        query: str,
        k: int = 4,
        filter_metadata: Optional[dict[str, Any]] = None,
    ) -> list[VectorStoreResult]:
        """Realiza búsqueda semántica por similitud."""
        if not self.is_initialized:
            raise RuntimeError("El índice no está inicializado")

        logger.debug("Buscando '%s' con k=%d", query[:50], k)

        docs = self._vector_store.similarity_search_with_score(
            query=query,
            k=k,
            filter=filter_metadata,
        )

        results = []
        for idx, (doc, score) in enumerate(docs):
            results.append(
                VectorStoreResult(
                    text=doc.page_content,
                    metadata=doc.metadata,
                    score=float(score),
                    index=idx,
                )
            )

        logger.info("Búsqueda retornó %d resultados", len(results))
        return results

    def similarity_search_by_vector(
        self,
        embedding: list[float],
        k: int = 4,
    ) -> list[VectorStoreResult]:
        """Búsqueda por vector de embedding precalculado."""
        if not self.is_initialized:
            raise RuntimeError("El índice no está inicializado")

        docs = self._vector_store.similarity_search_by_vector(
            embedding=embedding,
            k=k,
        )

        return [
            VectorStoreResult(
                text=doc.page_content,
                metadata=doc.metadata,
                score=0.0,
                index=idx,
            )
            for idx, doc in enumerate(docs)
        ]

    def max_marginal_relevance_search(
        self,
        query: str,
        k: int = 4,
        fetch_k: int = 20,
    ) -> list[VectorStoreResult]:
        """Búsqueda por relevancia marginal máxima para diversidad."""
        if not self.is_initialized:
            raise RuntimeError("El índice no está inicializado")

        docs = self._vector_store.max_marginal_relevance_search(
            query=query,
            k=k,
            fetch_k=fetch_k,
        )

        return [
            VectorStoreResult(
                text=doc.page_content,
                metadata=doc.metadata,
                score=0.0,
                index=idx,
            )
            for idx, doc in enumerate(docs)
        ]

    def get_index_stats(self) -> dict[str, Any]:
        """Retorna estadísticas del índice."""
        if not self.is_initialized:
            return {"initialized": False}

        return {
            "initialized": True,
            "index_name": self.config.index_name,
            "num_documents": self._vector_store.index.ntotal,
            "dimension": self._vector_store.index.d,
            "distance_strategy": self.config.distance_strategy,
        }

    def save_index(self, path: Optional[str] = None) -> None:
        """Persiste el índice a disco."""
        if not self.is_initialized:
            raise RuntimeError("No hay índice para persistir")

        save_path = path or self.config.persist_directory
        if not save_path:
            raise ValueError("Se requiere un directorio de persistencia")

        self._vector_store.save_local(save_path)
        logger.info("Índice persistido en %s", save_path)

    def load_index(self, path: Optional[str] = None) -> None:
        """Carga un índice desde disco."""
        load_path = path or self.config.persist_directory
        if not load_path:
            raise ValueError("Se requiere un directorio de carga")

        embeddings = self.embeddings_service._client
        self._vector_store = FAISS.load_local(
            load_path,
            embeddings,
            allow_dangerous_deserialization=self.config.allow_dangerous_deserialization,
        )
        self._initialized = True
        logger.info("Índice cargado desde %s", load_path)

    def delete_index(self) -> None:
        """Elimina el índice de memoria."""
        self._vector_store = None
        self._initialized = False
        logger.info("Índice eliminado de memoria")


def create_vector_store_service(
    provider: Optional[str] = None,
    persist_directory: Optional[str] = None,
) -> VectorStoreService:
    """Factory para crear el servicio de store vectorial."""
    config = None
    if provider or persist_directory:
        config = VectorStoreConfig(
            provider=provider or "faiss",
            persist_directory=persist_directory,
        )
    return VectorStoreService(config=config)