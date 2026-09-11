"""Excepciones personalizadas para el dominio de consulta normativa."""

from typing import Any, Optional


class PragmaNormativaError(Exception):
    """Excepción base para errores del sistema de consulta normativa."""

    def __init__(
        self,
        message: str,
        error_code: str = "UNKNOWN_ERROR",
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}

    def to_dict(self) -> dict[str, Any]:
        """Convierte la excepción a un diccionario serializable."""
        return {
            "error": self.__class__.__name__,
            "message": self.message,
            "error_code": self.error_code,
            "details": self.details,
        }


class RetrievalError(PragmaNormativaError):
    """Error durante la recuperación de contexto desde la base de conocimiento."""

    def __init__(
        self,
        message: str = "Error retrieving context from knowledge base",
        error_code: str = "RETRIEVAL_ERROR",
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, error_code, details)


class InvalidQueryError(PragmaNormativaError):
    """Error cuando la consulta del usuario no es válida o está vacía."""

    def __init__(
        self,
        message: str = "Invalid query: query cannot be empty or malformed",
        error_code: str = "INVALID_QUERY",
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, error_code, details)


class VectorStoreError(PragmaNormativaError):
    """Error en la operación del store vectorial."""

    def __init__(
        self,
        message: str = "Error interacting with vector store",
        error_code: str = "VECTOR_STORE_ERROR",
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, error_code, details)


class EmbeddingError(PragmaNormativaError):
    """Error durante la generación de embeddings."""

    def __init__(
        self,
        message: str = "Error generating embeddings for query",
        error_code: str = "EMBEDDING_ERROR",
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, error_code, details)


class GenerationError(PragmaNormativaError):
    """Error durante la generación de respuesta por el modelo."""

    def __init__(
        self,
        message: str = "Error generating response from model",
        error_code: str = "GENERATION_ERROR",
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, error_code, details)


class BedrockInvocationError(PragmaNormativaError):
    """Error al invocar el modelo de Bedrock."""

    def __init__(
        self,
        message: str = "Error invoking AWS Bedrock model",
        error_code: str = "BEDROCK_INVOCATION_ERROR",
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, error_code, details)


class ContextRetrievalError(RetrievalError):
    """Error específico cuando no se puede recuperar contexto relevante."""

    def __init__(
        self,
        message: str = "No relevant context found for the query",
        error_code: str = "CONTEXT_RETRIEVAL_ERROR",
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, error_code, details)


class PromptTemplateError(PragmaNormativaError):
    """Error en la construcción o renderizado del prompt."""

    def __init__(
        self,
        message: str = "Error constructing prompt template",
        error_code: str = "PROMPT_TEMPLATE_ERROR",
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, error_code, details)


class ValidationError(PragmaNormativaError):
    """Error de validación de datos o parámetros."""

    def __init__(
        self,
        message: str = "Validation failed for input data",
        error_code: str = "VALIDATION_ERROR",
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, error_code, details)


class ConfigurationError(PragmaNormativaError):
    """Error de configuración del sistema."""

    def __init__(
        self,
        message: str = "Configuration error in system setup",
        error_code: str = "CONFIGURATION_ERROR",
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, error_code, details)


class ModelTimeoutError(BedrockInvocationError):
    """Error específico cuando el modelo supera el tiempo de espera."""

    def __init__(
        self,
        message: str = "Model request timed out",
        error_code: str = "MODEL_TIMEOUT",
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, error_code, details)


class ModelThrottlingError(BedrockInvocationError):
    """Error específico cuando el modelo está siendo throttled por AWS."""

    def __init__(
        self,
        message: str = "Model request throttled by AWS",
        error_code: str = "MODEL_THROTTLING",
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, error_code, details)


class EvaluationError(PragmaNormativaError):
    """Error durante la evaluación de respuestas."""

    def __init__(
        self,
        message: str = "Error during response evaluation",
        error_code: str = "EVALUATION_ERROR",
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, error_code, details)


class OutputValidationError(PragmaNormativaError):
    """Error cuando la salida del modelo no cumple el esquema esperado."""

    def __init__(
        self,
        message: str = "Model output does not match expected schema",
        error_code: str = "OUTPUT_VALIDATION_ERROR",
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, error_code, details)