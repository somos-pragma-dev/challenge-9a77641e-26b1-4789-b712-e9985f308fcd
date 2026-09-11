import logging
import time
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config.settings import get_settings
from app.utils.exceptions import (
    BedrockInvocationError,
    ContextRetrievalError,
    InvalidQueryError,
    VectorStoreError,
)
from app.utils.logging import configure_logging, get_logger


@asynccontextmanager
async def lifespan(app: FastAPI) -> Any:
    settings = get_settings()
    configure_logging(settings.log_level)
    logger = get_logger(__name__)
    logger.info(
        "Aplicación de consulta normativa iniciada",
        extra={
            "environment": settings.environment,
            "bedrock_model_id": settings.bedrock_model_id,
        },
    )
    yield
    logger.info("Aplicación de consulta normativa detenida")


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="API de Consulta Normativa PragmaFintech",
        description="Sistema de recuperación y generación de respuestas sobre normativa interna",
        version="0.1.0",
        docs_url="/docs" if settings.environment != "production" else None,
        redoc_url="/redoc" if settings.environment != "production" else None,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def log_requests(request: Request, call_next: Any) -> Response:
        logger = get_logger(__name__)
        start_time = time.perf_counter()
        request_id = request.headers.get("X-Request-ID", f"req-{int(time.time() * 1000)}")

        logger.info(
            "Solicitud recibida",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "client_host": request.client.host if request.client else None,
            },
        )

        try:
            response = await call_next(request)
            process_time = (time.perf_counter() - start_time) * 1000

            logger.info(
                "Solicitud procesada",
                extra={
                    "request_id": request_id,
                    "status_code": response.status_code,
                    "process_time_ms": round(process_time, 2),
                },
            )

            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
            return response

        except Exception as exc:
            process_time = (time.perf_counter() - start_time) * 1000
            logger.error(
                "Error procesando solicitud",
                extra={
                    "request_id": request_id,
                    "error_type": type(exc).__name__,
                    "error_message": str(exc),
                    "process_time_ms": round(process_time, 2),
                },
                exc_info=True,
            )
            raise

    @app.exception_handler(InvalidQueryError)
    async def invalid_query_handler(request: Request, exc: InvalidQueryError) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={
                "error": "consulta_invalida",
                "mensaje": exc.message,
                "detalle": exc.detail,
            },
        )

    @app.exception_handler(ContextRetrievalError)
    async def context_retrieval_handler(request: Request, exc: ContextRetrievalError) -> JSONResponse:
        return JSONResponse(
            status_code=502,
            content={
                "error": "recuperacion_contexto_fallida",
                "mensaje": exc.message,
                "detalle": exc.detail,
            },
        )

    @app.exception_handler(VectorStoreError)
    async def vector_store_handler(request: Request, exc: VectorStoreError) -> JSONResponse:
        return JSONResponse(
            status_code=503,
            content={
                "error": "almacenamiento_vectorial_no_disponible",
                "mensaje": exc.message,
            },
        )

    @app.exception_handler(BedrockInvocationError)
    async def bedrock_error_handler(request: Request, exc: BedrockInvocationError) -> JSONResponse:
        return JSONResponse(
            status_code=502,
            content={
                "error": "invocacion_modelo_fallida",
                "mensaje": exc.message,
                "retryable": exc.retryable,
            },
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger = get_logger(__name__)
        logger.critical(
            "Excepción no manejada",
            extra={
                "request_path": request.url.path,
                "exception_type": type(exc).__name__,
            },
            exc_info=True,
        )
        return JSONResponse(
            status_code=500,
            content={
                "error": "error_interno_servidor",
                "mensaje": "Ha ocurrido un error interno. Por favor contacte al administrador.",
            },
        )

    from app.api.endpoints import router as api_router
    app.include_router(api_router, prefix="/api/v1", tags=["consulta-normativa"])

    @app.get("/health")
    async def health_check() -> dict[str, Any]:
        return {
            "status": "healthy",
            "service": "consulta-normativa",
            "version": "0.1.0",
        }

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    settings = get_settings()
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.environment == "development",
        log_level=settings.log_level.lower(),
    )