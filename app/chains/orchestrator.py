import logging
from typing import Any, Optional

from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.schema import StrOutputParser
from pydantic import BaseModel, Field

from app.models.bedrock import BedrockClient, BedrockResponse
from app.retrieval.embeddings import create_embeddings_service
from app.retrieval.vector_store import (
    VectorStoreResult,
    create_vector_store_service,
)

logger = logging.getLogger(__name__)


class OrchestratorConfig(BaseModel):
    """Configuración del orquestador RAG."""

    max_context_docs: int = Field(default=4, description="Máximo de documentos en contexto")
    temperature: float = Field(default=0.7, description="Temperatura del modelo")
    max_tokens: int = Field(default=2048, description="Máximo de tokens en respuesta")
    retrieval_strategy: str = Field(default="similarity", description="Estrategia de recuperación")
    enable_reranking: bool = Field(default=False, description="Habilitar reordenamiento")


class OrchestratorInput(BaseModel):
    """Entrada para el orquestador."""

    query: str = Field(..., description="Consulta del usuario")
    context_filter: Optional[dict[str, Any]] = Field(default=None, description="Filtro de metadatos")
    conversation_history: Optional[list[dict[str, str]]] = Field(default=None, description="Historial de conversación")


class OrchestratorOutput(BaseModel):
    """Salida del orquestador RAG."""

    answer: str
    sources: list[dict[str, Any]]
    retrieved_documents: list[VectorStoreResult]
    metrics: dict[str, Any]


class RAGOrchestrator:
    """Orquestador del pipeline RAG: recuperación, generación y post-procesamiento."""

    def __init__(
        self,
        config: Optional[OrchestratorConfig] = None,
        vector_store_service: Optional[Any] = None,
        bedrock_client: Optional[BedrockClient] = None,
    ) -> None:
        self.config = config or OrchestratorConfig()
        self.vector_store = vector_store_service or create_vector_store_service()
        self.embeddings_service = create_embeddings_service()
        self.bedrock_client = bedrock_client or BedrockClient()
        self._prompt_template = self._build_prompt_template()

    def _build_prompt_template(self) -> ChatPromptTemplate:
        """Construye el template de prompt para generación de respuesta."""
        system_template = """Eres un asistente especializado en normativa de PragmaFintech.
Tu tarea es responder preguntas basándote únicamente en el contexto proporcionado.

Instrucciones:
1. Utiliza únicamente la información del contexto para responder.
2. Si la respuesta no se encuentra en el contexto, indica que no tienes esa información.
3. Cita las fuentes cuando sea posible.
4. Sé conciso y profesional en tus respuestas.

Contexto:
{context}

Historial de conversación:
{history}

Pregunta: {question}"""

        return ChatPromptTemplate.from_messages(
            [
                HumanMessagePromptTemplate.from_template(system_template),
                HumanMessagePromptTemplate.from_template("{question}"),
            ]
        )

    def retrieve_context(
        self,
        query: str,
        context_filter: Optional[dict[str, Any]] = None,
    ) -> list[VectorStoreResult]:
        """Recupera documentos relevantes del store vectorial."""
        logger.info("Recuperando contexto para query: %s", query[:100])

        if self.config.retrieval_strategy == "mmr":
            results = self.vector_store.max_marginal_relevance_search(
                query=query,
                k=self.config.max_context_docs,
                fetch_k=self.config.max_context_docs * 3,
            )
        else:
            results = self.vector_store.similarity_search(
                query=query,
                k=self.config.max_context_docs,
                filter_metadata=context_filter,
            )

        logger.info("Recuperados %d documentos", len(results))
        return results

    def format_context(self, documents: list[VectorStoreResult]) -> str:
        """Formatea los documentos recuperados como contexto para el prompt."""
        context_parts = []
        for idx, doc in enumerate(documents, 1):
            source_info = f"[Fuente {idx}]: {doc.metadata.get('source', 'Desconocido')}"
            if doc.metadata.get("article"):
                source_info += f" - Artículo {doc.metadata['article']}"
            context_parts.append(f"{source_info}\n\n{doc.text}")

        return "\n\n---\n\n".join(context_parts)

    def format_history(
        self,
        history: Optional[list[dict[str, str]]],
    ) -> str:
        """Formatea el historial de conversación."""
        if not history:
            return "No hay historial previo."

        formatted = []
        for msg in history[-5:]:  # Últimos 5 mensajes
            role = msg.get("role", "user")
            content = msg.get("content", "")
            formatted.append(f"{role.capitalize()}: {content}")

        return "\n".join(formatted)

    def generate_response(
        self,
        query: str,
        context: str,
        history: str,
    ) -> BedrockResponse:
        """Genera la respuesta usando Bedrock."""
        prompt = self._prompt_template.format(
            context=context,
            history=history,
            question=query,
        )

        logger.debug("Prompt长度: %d caracteres", len(prompt))

        try:
            response = self.bedrock_client.invoke_model(
                prompt=prompt,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
            )
            return response
        except Exception as e:
            logger.error("Error en generación de respuesta: %s", str(e))
            raise

    def post_process_response(
        self,
        response: BedrockResponse,
        documents: list[VectorStoreResult],
    ) -> str:
        """Post-procesa la respuesta del modelo."""
        answer = response.content.strip()

        # Validar que la respuesta no sea vacía
        if not answer:
            logger.warning("Respuesta vacía del modelo")
            return "No fue posible generar una respuesta. Por favor, intenta nuevamente."

        # Añadir citas si hay documentos
        if documents:
            sources = [f"[{(i+1)}]" for i in range(len(documents))]
            answer += f"\n\nFuentes: {', '.join(sources)}"

        return answer

    def execute(self, input_data: OrchestratorInput) -> OrchestratorOutput:
        """Ejecuta el pipeline completo de RAG."""
        import time

        start_time = time.time()

        # Fase 1: Recuperación
        retrieved_docs = self.retrieve_context(
            query=input_data.query,
            context_filter=input_data.context_filter,
        )

        # Fase 2: Formateo de contexto
        context = self.format_context(retrieved_docs)
        history = self.format_history(input_data.conversation_history)

        # Fase 3: Generación
        response = self.generate_response(
            query=input_data.query,
            context=context,
            history=history,
        )

        # Fase 4: Post-procesamiento
        answer = self.post_process_response(response, retrieved_docs)

        # Métricas
        elapsed_time = time.time() - start_time
        metrics = {
            "elapsed_time_seconds": round(elapsed_time, 3),
            "num_retrieved_docs": len(retrieved_docs),
            "retrieval_strategy": self.config.retrieval_strategy,
            "model_latency_ms": response.latency_ms if hasattr(response, 'latency_ms') else None,
            "tokens_used": response.input_tokens + response.output_tokens if hasattr(response, 'input_tokens') else None,
        }

        # Formatear fuentes
        sources = [
            {
                "text": doc.text[:200] + "..." if len(doc.text) > 200 else doc.text,
                "metadata": doc.metadata,
                "score": doc.score,
            }
            for doc in retrieved_docs
        ]

        return OrchestratorOutput(
            answer=answer,
            sources=sources,
            retrieved_documents=retrieved_docs,
            metrics=metrics,
        )


def create_orchestrator(
    max_context_docs: Optional[int] = None,
    temperature: Optional[float] = None,
    retrieval_strategy: Optional[str] = None,
) -> RAGOrchestrator:
    """Factory para crear el orquestador RAG."""
    config = OrchestratorConfig(
        max_context_docs=max_context_docs or 4,
        temperature=temperature or 0.7,
        retrieval_strategy=retrieval_strategy or "similarity",
    )
    return RAGOrchestrator(config=config)