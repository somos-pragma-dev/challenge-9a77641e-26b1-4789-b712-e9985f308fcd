import os
from functools import lru_cache
from typing import Any, Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    environment: Literal["development", "staging", "production"] = Field(
        default="development",
        description="Entorno de ejecución de la aplicación",
    )

    host: str = Field(default="0.0.0.0", description="Host donde corre el servidor")
    port: int = Field(default=8000, description="Puerto del servidor")

    log_level: str = Field(default="INFO", description="Nivel de logging")

    cors_origins: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        description="Orígenes permitidos para CORS",
    )

    aws_region: str = Field(default="us-east-1", description="Región de AWS")
    aws_profile: str | None = Field(default=None, description="Perfil de AWS credentials")

    bedrock_model_id: str = Field(
        default="anthropic.claude-3-sonnet-20240229-v1:0",
        description="Identificador del modelo en Bedrock",
    )
    bedrock_max_tokens: int = Field(
        default=2048,
        description="Máximo de tokens en respuesta del modelo",
    )
    bedrock_temperature: float = Field(
        default=0.7,
        description="Temperatura para generación",
    )
    bedrock_top_p: float = Field(
        default=0.9,
        description="Top P para generación",
    )

    vector_store_provider: Literal["pinecone", "qdrant", "in-memory"] = Field(
        default="in-memory",
        description="Proveedor de almacenamiento vectorial",
    )
    pinecone_api_key: str | None = Field(default=None, description="API Key de Pinecone")
    pinecone_environment: str | None = Field(default=None, description="Entorno de Pinecone")
    pinecone_index_name: str = Field(default="normativa-index", description="Nombre del índice")

    qdrant_url: str | None = Field(default=None, description="URL de Qdrant")
    qdrant_api_key: str | None = Field(default=None, description="API Key de Qdrant")
    qdrant_collection: str = Field(default="normativa", description="Nombre de colección")

    embeddings_model: str = Field(
        default="amazon.titan-embed-text-v1",
        description="Modelo para generar embeddings",
    )
    embeddings_dimension: int = Field(
        default=1536,
        description="Dimensión de los vectores de embedding",
    )

    retrieval_top_k: int = Field(
        default=5,
        description="Número de documentos a recuperar",
    )
    retrieval_similarity_threshold: float = Field(
        default=0.7,
        description="Umbral de similitud para recuperación",
    )

    prompt_template_version: str = Field(
        default="v1.0",
        description="Versión del template de prompt",
    )
    prompt_max_context_length: int = Field(
        default=8000,
        description="Máximo de tokens para contexto",
    )

    evaluation_enabled: bool = Field(
        default=True,
        description="Habilitar evaluación automática",
    )
    evaluation_sample_size: int = Field(
        default=100,
        description="Tamaño de muestra para evaluación",
    )

    rate_limit_requests_per_minute: int = Field(
        default=60,
        description="Límite de requests por minuto",
    )

    cache_ttl_seconds: int = Field(
        default=3600,
        description="TTL para cache de respuestas",
    )

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Any) -> list[str]:
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        v_upper = v.upper()
        if v_upper not in valid_levels:
            raise ValueError(f"log_level debe ser uno de {valid_levels}")
        return v_upper

    @field_validator("bedrock_temperature")
    @classmethod
    def validate_temperature(cls, v: float) -> float:
        if not 0.0 <= v <= 1.0:
            raise ValueError("bedrock_temperature debe estar entre 0.0 y 1.0")
        return v

    @field_validator("bedrock_top_p")
    @classmethod
    def validate_top_p(cls, v: float) -> float:
        if not 0.0 <= v <= 1.0:
            raise ValueError("bedrock_top_p debe estar entre 0.0 y 1.0")
        return v

    def get_aws_credentials(self) -> dict[str, Any]:
        credentials: dict[str, Any] = {"region_name": self.aws_region}
        if self.aws_profile:
            credentials["profile_name"] = self.aws_profile
        return credentials

    def is_production(self) -> bool:
        return self.environment == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()