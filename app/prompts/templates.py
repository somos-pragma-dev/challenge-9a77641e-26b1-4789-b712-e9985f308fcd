package app.prompts

from typing import Optional
from enum import Enum


class PromptVersion(str, Enum):
    """Versiones disponibles de los templates de prompts."""
    V1_0 = "1.0"
    V1_1 = "1.1"
    V2_0 = "2.0"


class QueryType(str, Enum):
    """Tipos de consulta normativa soportados."""
    OPEN = "open"
    SPECIFIC = "specific"
    PROCEDURAL = "procedural"
    POLICY = "policy"
    COMPLIANCE = "compliance"


class PromptTemplate:
    """Template de prompt con soporte para placeholders."""
    
    def __init__(self, template: str, version: PromptVersion, query_type: QueryType):
        self._template = template
        self._version = version
        self._query_type = query_type
    
    def render(self, context: str, query: str, **kwargs: str) -> str:
        """Renderiza el template con los valores proporcionados."""
        return self._template.format(
            context=context,
            query=query,
            **kwargs
        )
    
    @property
    def version(self) -> PromptVersion:
        return self._version
    
    @property
    def query_type(self) -> QueryType:
        return self._query_type


SYSTEM_PROMPT_BASE = """Eres un asistente especializado en consultas sobre normativa interna de PragmaFintech. 
Tu objetivo es proporcionar respuestas precisas, claras y basadas únicamente en los documentos proporcionados.

Instrucciones importantes:
1. Utiliza EXCLUSIVAMENTE la información del contexto proporcionado
2. Si no tienes suficiente información, indícalo claramente
3. Cita las fuentes cuando sea apropiado
4. Responde en el mismo idioma de la consulta
5. Estructura tu respuesta de manera clara y organizada

Contexto relevante:
{context}

Consulta del usuario:
{query}

Responde de forma estructurada:"""

SYSTEM_PROMPT_V1_0 = SYSTEM_PROMPT_BASE + """

Respuesta:
"""

SYSTEM_PROMPT_V1_1 = SYSTEM_PROMPT_BASE + """

Antes de responder, considera:
- ¿La respuesta está basada en los documentos proporcionados?
- ¿Se han citado las fuentes relevantes?
- ¿La respuesta es completa y precisa?

Respuesta estructurada:
"""

SYSTEM_PROMPT_V2_0 = """Eres un asistente especializado en consultas sobre normativa interna de PragmaFintech.

POLÍTICAS DE RESPUESTA:
1. Solo utiliza información del contexto proporcionado
2. Indica claramente cuando la información es insuficiente
3. Incluye referencias a las fuentes
4. Mantén un tono profesional y preciso
5. Estructura las respuestas de forma clara

CONTEXTO DISPONIBLE:
{context}

CONSULTA:
{query}

INSTRUCCIONES DE FORMATO:
- Responde en el idioma de la consulta
- Usa viñetas para listas de información
- Destaca los puntos clave
- Incluye ejemplos cuando sea relevante

RESPUESTA:"""

QUERY_SPECIFIC_PROMPT = """Basándote únicamente en el siguiente contexto de documentos normativos, responde la consulta específica del usuario.

Contexto:
{context}

Consulta: {query}

Proporciona una respuesta directa y precisa. Si la respuesta no se encuentra en el contexto, indica que no es posible responder con la información disponible.

Respuesta:"""

QUERY_OPEN_PROMPT = """Analiza el siguiente contexto normativo y proporciona una respuesta comprehensiva a la consulta del usuario.

Documentos de referencia:
{context}

Consulta: {query}

Tu respuesta debe:
- Ser completa y detallada
- Incluir todas las políticas relevantes
- Proporcionar ejemplos prácticos
- Citar las fuentes utilizadas

Respuesta detallada:"""

QUERY_PROCEDURAL_PROMPT = """Para consultas sobre procedimientos, proporciona pasos claros y secuenciales.

Procedimientos aplicables:
{context}

Consulta del usuario: {query}

Estructura tu respuesta siguiendo el formato:
1. Requisitos previos
2. Pasos a seguir
3. Documentación necesaria
4. Tiempos estimados
5. Contactos de soporte

Procedimiento:"""

QUERY_POLICY_PROMPT = """Consulta sobre políticas corporativas.

Políticas aplicables:
{context}

Consulta: {query}

Responde indicando:
- Alcance de la política
- Obligaciones y responsabilidades
- Consecuencias del incumplimiento
- Excepciones aplicables

Política:"""

QUERY_COMPLIANCE_PROMPT = """Consulta sobre cumplimiento normativo.

Documentación de cumplimiento:
{context}

Consulta: {query}

Proporciona información sobre:
- Requisitos regulatorios aplicables
- Obligaciones de cumplimiento
- Plazos y fechas límite
- Procedimientos de reporte
- Sanciones por incumplimiento

Cumplimiento:"""

EVALUATION_PROMPT = """Eres un evaluador experto de respuestas generadas por modelos de lenguaje.

Evalúa la siguiente respuesta según los criterios:
- Fidelidad al contexto
- Relevancia de la respuesta
- Coherencia y claridad
- Completitud

Consulta original: {query}

Contexto utilizado: {context}

Respuesta a evaluar: {answer}

Proporciona una evaluación numérica de 0 a 1 para cada criterio y justifica tu puntuación.

Evaluación:"""

FAITHFULNESS_PROMPT = """Evalúa la fidelidad de la respuesta respecto al contexto proporcionado.

Contexto fuente: {context}

Respuesta generada: {answer}

Responde con un valor entre 0 y 1 donde:
- 1.0: La respuesta está completamente respaldada por el contexto
- 0.5: La respuesta está parcialmente respaldada
- 0.0: La respuesta contradice o no tiene relación con el contexto

Valor de fidelidad:"""

_RETRIEVAL_EVALUATION_PROMPT = """Evalúa la calidad de la recuperación de documentos.

Consulta: {query}

Documentos recuperados: {retrieved_docs}

Evalúa si los documentos recuperados son relevantes para responder la consulta.

Precision (0-1):"""


class PromptTemplateRegistry:
    """Registro centralizado de templates de prompts versionados."""
    
    def __init__(self):
        self._templates: dict[PromptVersion, dict[QueryType, PromptTemplate]] = {
            PromptVersion.V1_0: {
                QueryType.OPEN: PromptTemplate(QUERY_OPEN_PROMPT, PromptVersion.V1_0, QueryType.OPEN),
                QueryType.SPECIFIC: PromptTemplate(QUERY_SPECIFIC_PROMPT, PromptVersion.V1_0, QueryType.SPECIFIC),
                QueryType.PROCEDURAL: PromptTemplate(QUERY_PROCEDURAL_PROMPT, PromptVersion.V1_0, QueryType.PROCEDURAL),
                QueryType.POLICY: PromptTemplate(QUERY_POLICY_PROMPT, PromptVersion.V1_0, QueryType.POLICY),
                QueryType.COMPLIANCE: PromptTemplate(QUERY_COMPLIANCE_PROMPT, PromptVersion.V1_0, QueryType.COMPLIANCE),
            },
            PromptVersion.V1_1: {
                QueryType.OPEN: PromptTemplate(QUERY_OPEN_PROMPT, PromptVersion.V1_1, QueryType.OPEN),
                QueryType.SPECIFIC: PromptTemplate(QUERY_SPECIFIC_PROMPT, PromptVersion.V1_1, QueryType.SPECIFIC),
                QueryType.PROCEDURAL: PromptTemplate(QUERY_PROCEDURAL_PROMPT, PromptVersion.V1_1, QueryType.PROCEDURAL),
                QueryType.POLICY: PromptTemplate(QUERY_POLICY_PROMPT, PromptVersion.V1_1, QueryType.POLICY),
                QueryType.COMPLIANCE: PromptTemplate(QUERY_COMPLIANCE_PROMPT, PromptVersion.V1_1, QueryType.COMPLIANCE),
            },
            PromptVersion.V2_0: {
                QueryType.OPEN: PromptTemplate(QUERY_OPEN_PROMPT, PromptVersion.V2_0, QueryType.OPEN),
                QueryType.SPECIFIC: PromptTemplate(QUERY_SPECIFIC_PROMPT, PromptVersion.V2_0, QueryType.SPECIFIC),
                QueryType.PROCEDURAL: PromptTemplate(QUERY_PROCEDURAL_PROMPT, PromptVersion.V2_0, QueryType.PROCEDURAL),
                QueryType.POLICY: PromptTemplate(QUERY_POLICY_PROMPT, PromptVersion.V2_0, QueryType.POLICY),
                QueryType.COMPLIANCE: PromptTemplate(QUERY_COMPLIANCE_PROMPT, PromptVersion.V2_0, QueryType.COMPLIANCE),
            },
        }
        self._system_prompts: dict[PromptVersion, str] = {
            PromptVersion.V1_0: SYSTEM_PROMPT_V1_0,
            PromptVersion.V1_1: SYSTEM_PROMPT_V1_1,
            PromptVersion.V2_0: SYSTEM_PROMPT_V2_0,
        }
    
    def get_system_prompt(self, version: PromptVersion = PromptVersion.V2_0) -> str:
        """Obtiene el prompt de sistema para la versión especificada."""
        return self._system_prompts.get(version, self._system_prompts[PromptVersion.V2_0])
    
    def get_template(
        self, 
        query_type: QueryType, 
        version: PromptVersion = PromptVersion.V2_0
    ) -> PromptTemplate:
        """Obtiene el template para el tipo de consulta y versión especificada."""
        return self._templates[version][query_type]
    
    def get_evaluation_prompt(self, eval_type: str = "comprehensive") -> str:
        """Obtiene el prompt de evaluación según el tipo."""
        if eval_type == "faithfulness":
            return FAITHFULNESS_PROMPT
        elif eval_type == "retrieval":
            return _RETRIEVAL_EVALUATION_PROMPT
        return EVALUATION_PROMPT
    
    def classify_query_type(self, query: str) -> QueryType:
        """Clasifica el tipo de consulta basándose en palabras clave."""
        query_lower = query.lower()
        
        if any(kw in query_lower for kw in ["procedimiento", "cómo hacer", "pasos", "proceso"]):
            return QueryType.PROCEDURAL
        elif any(kw in query_lower for kw in ["política", "políticas", "regla", "norma"]):
            return QueryType.POLICY
        elif any(kw in query_lower for kw in ["cumplimiento", "regulación", "obligación", "legal"]):
            return QueryType.COMPLIANCE
        elif any(kw in query_lower for kw in ["¿qué es", "¿cuál es", "explique", "describe"]):
            return QueryType.OPEN
        else:
            return QueryType.SPECIFIC


_registry: Optional[PromptTemplateRegistry] = None


def get_prompt_registry() -> PromptTemplateRegistry:
    """Obtiene la instancia singleton del registro de prompts."""
    global _registry
    if _registry is None:
        _registry = PromptTemplateRegistry()
    return _registry


import logging
from typing import Any, Optional

import numpy as np
from langchain_aws import BedrockEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings

from app.config.settings import get_settings

logger = logging.getLogger(__name__)


class EmbeddingsConfig:
    """Configuración del modelo de embeddings."""

    def __init__(
        self,
        provider: str = "bedrock",
        model_id: str = "amazon.titan-embed-text-v1",
        normalize: bool = True,
        batch_size: int = 100,
    ) -> None:
        self.provider = provider
        self.model_id = model_id
        self.normalize = normalize
        self.batch_size = batch_size


class EmbeddingsService:
    """Servicio para generar embeddings de textos usando Bedrock o HuggingFace."""

    def __init__(self, config: Optional[EmbeddingsConfig] = None) -> None:
        self.settings = get_settings()
        self.config = config or self._default_config()
        self._client = self._initialize_client()

    def _default_config(self) -> EmbeddingsConfig:
        """Configuración por defecto usando Bedrock Titan."""
        return EmbeddingsConfig(
            provider=self.settings.EMBEDDING_PROVIDER,
            model_id=self.settings.EMBEDDING_MODEL_ID,
            normalize=True,
            batch_size=self.settings.EMBEDDING_BATCH_SIZE,
        )

    def _initialize_client(self) -> Any:
        """Inicializa el cliente de embeddings según el proveedor configurado."""
        if self.config.provider == "bedrock":
            return self._init_bedrock_client()
        elif self.config.provider == "huggingface":
            return self._init_huggingface_client()
        else:
            raise ValueError(f"Proveedor de embeddings no soportado: {self.config.provider}")

    def _init_bedrock_client(self) -> BedrockEmbeddings:
        """Inicializa cliente de Bedrock para embeddings."""
        credentials = self.settings.get_aws_credentials()
        return BedrockEmbeddings(
            client=self._create_bedrock_runtime(credentials),
            model_id=self.config.model_id,
            normalize=self.config.normalize,
        )

    def _create_bedrock_runtime(self, credentials: dict[str, Any]) -> Any:
        """Crea el cliente de Bedrock Runtime."""
        import boto3

        return boto3.client(
            "bedrock-runtime",
            aws_access_key_id=credentials["aws_access_key_id"],
            aws_secret_access_key=credentials["aws_secret_access_key"],
            region_name=self.settings.AWS_REGION,
        )

    def _init_huggingface_client(self) -> HuggingFaceEmbeddings:
        """Inicializa cliente de HuggingFace para embeddings."""
        return HuggingFaceEmbeddings(
            model_name=self.config.model_id,
            model_kwargs={"normalize_embeddings": self.config.normalize},
            encode_kwargs={"batch_size": self.config.batch_size},
        )

    def embed_query(self, text: str) -> list[float]:
        """Genera embedding para una consulta individual."""
        try:
            embedding = self._client.embed_query(text)
            logger.debug(
                "Embedding generado para consulta de %d caracteres",
                len(text),
            )
            return embedding
        except Exception as e:
            logger.error("Error al generar embedding: %s", str(e))
            raise

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Genera embeddings para una lista de documentos."""
        try:
            embeddings = self._client.embed_documents(texts)
            logger.info("Embeddings generados para %d documentos", len(texts))
            return embeddings
        except Exception as e:
            logger.error("Error al generar embeddings por lotes: %s", str(e))
            raise

    def embed_with_metadata(
        self,
        texts: list[str],
        metadatos: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Genera embeddings asociando metadatos a cada documento."""
        embeddings = self.embed_documents(texts)
        return [
            {"embedding": emb, "text": text, "metadata": meta}
            for emb, text, meta in zip(embeddings, texts, metadatos)
        ]

    def get_embedding_dimension(self) -> int:
        """Retorna la dimensión de los vectores de embedding."""
        test_embedding = self.embed_query("test")
        return len(test_embedding)

    def validate_embedding_quality(self, texts: list[str]) -> dict[str, Any]:
        """Valida la calidad de los embeddings generados."""
        embeddings = self.embed_documents(texts)
        embeddings_array = np.array(embeddings)

        # Calcular similitud coseno entre pares
        norms = np.linalg.norm(embeddings_array, axis=1, keepdims=True)
        normalized = embeddings_array / (norms + 1e-8)
        similarity_matrix = np.dot(normalized, normalized.T)

        # Métricas de diversidad
        mean_similarity = np.mean(similarity_matrix[np.triu_indices(len(texts), k=1)])

        return {
            "dimension": len(embeddings[0]),
            "num_documents": len(texts),
            "mean_similarity": float(mean_similarity),
            "min_similarity": float(np.min(similarity_matrix[np.triu_indices(len(texts), k=1)])),
            "max_similarity": float(np.max(similarity_matrix[np.triu_indices(len(texts), k=1)])),
        }


def create_embeddings_service(
    provider: Optional[str] = None,
    model_id: Optional[str] = None,
) -> EmbeddingsService:
    """Factory para crear el servicio de embeddings."""
    config = None
    if provider or model_id:
        config = EmbeddingsConfig(
            provider=provider or "bedrock",
            model_id=model_id or "amazon.titan-embed-text-v1",
        )
    return EmbeddingsService(config=config)