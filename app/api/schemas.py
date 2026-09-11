package app.api

from typing import Any, Optional
from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class QueryRequest(BaseModel):
    """Solicitud de consulta normativa al sistema RAG."""
    
    query: str = Field(
        ..., 
        min_length=3, 
        max_length=1000,
        description="Consulta del usuario sobre normativa interna",
        examples=["¿Cuáles son los requisitos para solicitar vacaciones?", "¿Cuál es la política de gastos de viaje?"]
    )
    session_id: Optional[str] = Field(
        None, 
        max_length=64,
        description="Identificador de sesión para trazabilidad"
    )
    language: str = Field(
        default="es",
        pattern="^(es|en)$",
        description="Idioma de la respuesta"
    )
    include_sources: bool = Field(
        default=True,
        description="Incluir referencias a los documentos fuente en la respuesta"
    )
    max_context_docs: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Número máximo de documentos de contexto a recuperar"
    )
    
    @field_validator("query")
    @classmethod
    def query_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("La consulta no puede estar vacía o contener solo espacios")
        return v.strip()


class SourceDocument(BaseModel):
    """Documento fuente recuperado del vector store."""
    
    doc_id: str = Field(..., description="Identificador único del documento")
    title: str = Field(..., description="Título del documento fuente")
    content: str = Field(..., description="Contenido relevante del documento")
    relevance_score: float = Field(
        ..., 
        ge=0.0, 
        le=1.0,
        description="Puntuación de relevancia del documento"
    )
    category: Optional[str] = Field(None, description="Categoría del documento")
    last_updated: Optional[datetime] = Field(None, description="Fecha de última actualización")


class NormativeResponse(BaseModel):
    """Respuesta del sistema de consulta normativa."""
    
    query: str = Field(..., description="Consulta original del usuario")
    answer: str = Field(..., description="Respuesta generada por el modelo")
    sources: list[SourceDocument] = Field(
        default_factory=list,
        description="Documentos fuente utilizados para generar la respuesta"
    )
    model_used: str = Field(..., description="Modelo de Bedrock utilizado")
    tokens_consumed: int = Field(..., ge=0, description="Total de tokens consumidos")
    latency_ms: float = Field(..., ge=0, description="Latencia de la consulta en milisegundos")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp de la respuesta")
    session_id: Optional[str] = Field(None, description="Identificador de sesión")
    confidence: Optional[float] = Field(
        None, 
        ge=0.0, 
        le=1.0,
        description="Nivel de confianza de la respuesta"
    )


class EvaluationRequest(BaseModel):
    """Solicitud de evaluación de una respuesta generada."""
    
    query: str = Field(..., min_length=3, max_length=1000, description="Consulta original")
    generated_answer: str = Field(..., min_length=1, description="Respuesta generada a evaluar")
    reference_answer: Optional[str] = Field(
        None, 
        description="Respuesta de referencia para cálculo de métricas supervisadas"
    )
    sources: list[SourceDocument] = Field(
        default_factory=list,
        description="Documentos fuente utilizados"
    )
    eval_type: str = Field(
        default="comprehensive",
        pattern="^(comprehensive|faithfulness|answer_quality|retrieval)$",
        description="Tipo de evaluación a realizar"
    )


class EvaluationMetrics(BaseModel):
    """Métricas de evaluación de la respuesta."""
    
    faithfulness: float = Field(..., ge=0.0, le=1.0, description="Grado de fidelidad a las fuentes")
    answer_quality: float = Field(..., ge=0.0, le=1.0, description="Calidad general de la respuesta")
    relevance: float = Field(..., ge=0.0, le=1.0, description="Relevancia semántica")
    coherence: float = Field(..., ge=0.0, le=1.0, description="Coherencia de la respuesta")
    retrieval_precision: Optional[float] = Field(
        None, 
        ge=0.0, 
        le=1.0,
        description="Precisión de la recuperación de contexto"
    )
    retrieval_recall: Optional[float] = Field(
        None, 
        ge=0.0, 
        le=1.0,
        description="Recall de la recuperación de contexto"
    )


class EvaluationResponse(BaseModel):
    """Respuesta del sistema de evaluación."""
    
    query: str = Field(..., description="Consulta evaluada")
    metrics: EvaluationMetrics = Field(..., description="Métricas calculadas")
    overall_score: float = Field(..., ge=0.0, le=1.0, description="Puntuación global")
    feedback: list[str] = Field(
        default_factory=list,
        description="Retroalimentación textual sobre la respuesta"
    )
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp de la evaluación")
    evaluation_type: str = Field(..., description="Tipo de evaluación realizada")


class HealthCheckResponse(BaseModel):
    """Respuesta del endpoint de health check."""
    
    status: str = Field(..., description="Estado general del sistema")
    version: str = Field(..., description="Versión de la aplicación")
    services: dict[str, bool] = Field(..., description="Estado de los servicios dependientes")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ErrorDetail(BaseModel):
    """Detalle de un error específico."""
    
    error_type: str = Field(..., description="Tipo de error")
    message: str = Field(..., description="Mensaje descriptivo")
    details: Optional[dict[str, Any]] = Field(None, description="Detalles adicionales del error")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ErrorResponse(BaseModel):
    """Respuesta de error estandarizada."""
    
    error: ErrorDetail = Field(..., description="Detalles del error")
    request_id: Optional[str] = Field(None, description="ID de la solicitud para trazabilidad")