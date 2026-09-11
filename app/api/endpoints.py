package app.api

from typing import Any
from fastapi import APIRouter, HTTPException, status, Request
from fastapi.responses import JSONResponse

from app.api.schemas import (
    QueryRequest,
    NormativeResponse,
    EvaluationRequest,
    EvaluationResponse,
    HealthCheckResponse,
    ErrorResponse,
)
from app.config.settings import get_settings
from app.utils.exceptions import (
    InvalidQueryError,
    ContextRetrievalError,
    VectorStoreError,
    BedrockInvocationError,
)

router = APIRouter(prefix="/api/v1", tags=["consulta-normativa"])

settings = get_settings()


@router.post(
    "/query",
    response_model=NormativeResponse,
    summary="Consultar normativa",
    description="Recibe una consulta sobre normativa interna y retorna una respuesta generada con contexto recuperado",
    responses={
        200: {"description": "Consulta procesada exitosamente"},
        400: {"model": ErrorResponse, "description": "Consulta inválida"},
        422: {"model": ErrorResponse, "description": "Error de validación"},
        500: {"model": ErrorResponse, "description": "Error interno del servidor"},
        503: {"model": ErrorResponse, "description": "Servicio no disponible"},
    },
)
async def query_normativa(request: QueryRequest, http_request: Request) -> NormativeResponse:
    """
    Procesa una consulta normativa utilizando el pipeline RAG.
    
    El flujo incluye:
    1. Validación de la consulta
    2. Recuperación de contexto relevante del vector store
    3. Generación de respuesta usando Bedrock
    4. Retorno de respuesta con metadatos
    """
    try:
        orchestrator = http_request.app.state.orchestrator
        
        result = await orchestrator.process_query(
            query=request.query,
            session_id=request.session_id,
            language=request.language,
            include_sources=request.include_sources,
            max_context_docs=request.max_context_docs,
        )
        
        return NormativeResponse(**result)
        
    except InvalidQueryError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_type": "INVALID_QUERY",
                "message": str(e),
                "details": {"query_length": len(request.query)},
            },
        )
    except ContextRetrievalError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "error_type": "CONTEXT_RETRIEVAL_ERROR",
                "message": "No se pudo recuperar el contexto necesario",
                "details": {"original_error": str(e)},
            },
        )
    except VectorStoreError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "error_type": "VECTOR_STORE_ERROR",
                "message": "Error en el almacén vectorial",
                "details": {"original_error": str(e)},
            },
        )
    except BedrockInvocationError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "error_type": "BEDROCK_ERROR",
                "message": "Error al invocar el modelo de Bedrock",
                "details": {"original_error": str(e)},
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_type": "INTERNAL_ERROR",
                "message": "Error inesperado al procesar la consulta",
                "details": {"error": str(e)},
            },
        )


@router.post(
    "/evaluate",
    response_model=EvaluationResponse,
    summary="Evaluar respuesta",
    description="Evalúa la calidad de una respuesta generada utilizando métricas definidas",
    responses={
        200: {"description": "Evaluación completada"},
        400: {"model": ErrorResponse, "description": "Solicitud de evaluación inválida"},
        500: {"model": ErrorResponse, "description": "Error en la evaluación"},
    },
)
async def evaluate_response(request: EvaluationRequest, http_request: Request) -> EvaluationResponse:
    """
    Evalúa una respuesta generada según múltiples métricas.
    
    Métricas calculadas:
    - Faithfulness: grado de fidelidad a las fuentes
    - Answer Quality: calidad general de la respuesta
    - Relevance: relevancia semántica
    - Coherence: coherencia interna
    - Retrieval Precision/Recall: calidad de la recuperación
    """
    try:
        evaluator = http_request.app.state.evaluator
        
        result = await evaluator.evaluate(
            query=request.query,
            generated_answer=request.generated_answer,
            reference_answer=request.reference_answer,
            sources=[s.model_dump() for s in request.sources],
            eval_type=request.eval_type,
        )
        
        return EvaluationResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_type": "INVALID_EVALUATION_REQUEST",
                "message": str(e),
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_type": "EVALUATION_ERROR",
                "message": "Error al evaluar la respuesta",
                "details": {"error": str(e)},
            },
        )


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    summary="Verificar salud del sistema",
    description="Retorna el estado de salud de los servicios dependientes",
    responses={
        200: {"description": "Sistema saludable"},
        503: {"description": "Sistema con problemas"},
    },
)
async def health_check(http_request: Request) -> HealthCheckResponse:
    """
    Verifica el estado de los servicios:
    - Vector Store (Chroma)
    - Bedrock
    - Configuración
    """
    services_status = {"vector_store": False, "bedrock": False, "config": True}
    overall_status = "healthy"
    
    try:
        vector_store = http_request.app.state.vector_store
        services_status["vector_store"] = vector_store.is_available()
    except Exception:
        services_status["vector_store"] = False
        overall_status = "degraded"
    
    try:
        bedrock_client = http_request.app.state.bedrock_client
        services_status["bedrock"] = bedrock_client.check_model_availability()
    except Exception:
        services_status["bedrock"] = False
        overall_status = "degraded"
    
    if not all(services_status.values()):
        overall_status = "unhealthy"
    
    return HealthCheckResponse(
        status=overall_status,
        version="0.1.0",
        services=services_status,
    )


@router.get(
    "/models",
    summary="Listar modelos disponibles",
    description="Retorna la lista de modelos de Bedrock disponibles",
    responses={
        200: {"description": "Lista de modelos"},
    },
)
async def list_models(http_request: Request) -> dict[str, Any]:
    """Retorna información sobre los modelos disponibles en Bedrock."""
    return {
        "models": [
            {
                "id": settings.bedrock_model_id,
                "provider": "aws",
                "name": "Claude 3 Sonnet",
                "max_tokens": settings.max_tokens,
                "supported_features": ["streaming", "json"],
            }
        ],
        "default_model": settings.bedrock_model_id,
    }