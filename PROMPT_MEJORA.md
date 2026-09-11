# Prompt para Mejorar el Codigo Base

Copia y pega el contenido del bloque de abajo en un asistente de IA (Claude, ChatGPT)
para obtener un ZIP con el proyecto completo y arrancable.

Si preferis trabajar en tu editor con un agente local (Claude Code, Cursor, Copilot), usa `AGENTS.md` en vez de este archivo: dice lo mismo pero para que escriba los archivos en disco.

## Las dos reglas que no se negocian

1. **Completa el boilerplate.** Todo lo que el proyecto necesita para compilar y arrancar: manifiesto de dependencias, punto de entrada, configuracion, capa de interfaz, y las capas del patron arquitectonico declarado. Eso es andamiaje y es tu trabajo.
2. **NO resuelvas el reto.** Los entregables de las fases son el trabajo de la persona. El hueco pedagogico se deja como esta: el proyecto arranca, pero lo que el reto pide implementar NO esta implementado.

Dicho de otra forma: si algo impide compilar, arreglalo. Si algo es logica de negocio incompleta, validaciones ausentes, un secreto hardcodeado o un patron mejorable, dejalo exactamente como esta — es lo que la persona tiene que encontrar.

## Lo que le falta a este proyecto

Esto NO lo tenes que adivinar: salio de comparar el proyecto contra la arquitectura declarada del reto y de un analisis estatico del codigo. Completalo TODO.

### Archivos corruptos — arreglar primero

El contenido no corresponde a la extension. Regeneralos completos:

- `data/sample_data.json` — El contenido no corresponde a un archivo json. Hay que regenerarlo completo.

### Archivos que la arquitectura del reto declara y no estan

Creálos con implementacion real, en la capa que les corresponde:

- `app/retrieval/embeddings.py`
- `app/utils/logging.py`
- `tests/test_api.py`
- `infra/terraform/main.tf`

### Referencias colgando en el codigo que si esta

Cada una rompe la compilacion:

- `app/models/bedrock.py` — `BedrockInvocationError.info`: Se invoca `info` sobre `BedrockInvocationError`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- `app/models/bedrock.py` — `BedrockInvocationError.debug`: Se invoca `debug` sobre `BedrockInvocationError`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- `app/models/bedrock.py` — `BedrockInvocationError.error`: Se invoca `error` sobre `BedrockInvocationError`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- `app/models/bedrock.py` — `BedrockInvocationError.critical`: Se invoca `critical` sobre `BedrockInvocationError`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- `app/models/bedrock.py` — `BedrockInvocationError.warning`: Se invoca `warning` sobre `BedrockInvocationError`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.

## Como saber que terminaste

```bash
pip install -r requirements.txt && pytest -q
```

Ese comando corriendo sin errores es la definicion de "listo".

---

```
## Briefing del reto (autoridad)
Este bloque manda sobre los archivos adjuntos. El stack y el rol salen de AQUÍ, no de un topic genérico ni de markdown placeholder.

### Perfil
Chapter Ciencia de Datos, Especialidad Ingeniero de IA, Tecnología AWS Bedrock, Senior

### Brecha de conocimiento
Construye soluciones sobre modelos generativos con recuperacion de contexto, salida estructurada y evaluacion medible

### Misión / candidato
Responder consultas sobre la normativa interna

### Reto
- Tema: Aplicaciones sobre modelos generativos
- Seniority: senior-l2
- Tipo: practical
- Título: Desarrollo de una solución de consulta normativa utilizando modelos generativos
- Tiempo estimado: 4 semanas

### Fases (trabajo del HUMANO — PROHIBIDO completarlas)
No implementes estos entregables. Dejalos como hueco pedagógico. El asistente solo materializa el proyecto arrancable para que el participante pueda trabajar.
- Fase 1: Definición del contexto y recopilación de datos — objetivo: Identificar las fuentes de información relevantes y recopilar los datos necesarios para entrenar el modelo. — entregable (NO resolver): Documento que describe las fuentes de información y los datos recopilados.
- Fase 2: Entrenamiento del modelo generativo — objetivo: Entrenar un modelo generativo utilizando los datos recopilados en la fase anterior. — entregable (NO resolver): Modelo generativo entrenado y evaluado.
- Fase 3: Integración y evaluación del sistema — objetivo: Integrar el modelo generativo en un sistema de consultas y evaluar su rendimiento en un entorno real. — entregable (NO resolver): Sistema de consultas integrado y evaluado.

Eres un asistente experto en análisis, corrección y generación de archivos de cualquier tipo:
código fuente, documentación, hojas de cálculo, documentos Word, configuraciones, entre otros.
Voy a enviarte una cadena de texto que contiene uno o más archivos. Cada archivo está delimitado por un marcador con el siguiente formato:
// === ARCHIVO: ruta/del/archivo.extension ===
o también puede aparecer como:
## === ARCHIVO: ruta/del/archivo.extension ===
Lo que sigue al marcador puede ser:

El contenido real del archivo (código, texto, YAML, etc.)
Una descripción en lenguaje natural de lo que debe contener el archivo


TU TAREA
PASO 0 — ¿Esto es un proyecto o una carcasa?
Antes de extraer archivos, leé el Briefing (si está) y diagnosticá el adjunto.

Es CARCASA si ocurre CUALQUIERA de estas:
- No hay manifiesto de dependencias del stack del briefing (manifest.json de VTEX IO / package.json / pom.xml / build.gradle / requirements.txt / go.mod / *.tf / *.csproj, según corresponda)
- Hay un "binario" que en realidad es un comentario ("no puede ser mostrado como texto plano", placeholder .fig/.docx vacío)
- Los markdowns ya completan entregables de fases posteriores ("se implementó fade-in", lista de áreas ya resuelta)

Si es CARCASA:
- MATERIALIZÁ un proyecto que arranca en el stack del briefing (VTEX IO Store Framework, Angular, Terraform, pytest, Nest, etc.). Incluí manifiesto, punto de entrada y capa de interfaz reales.
- NO copies los markdowns de "solución" como si fueran el producto. Son ruido de generación.
- NO resuelvas las fases del briefing (están marcadas PROHIBIDO). Dejá el hueco pedagógico: el flujo existe, las microinteracciones/calidad/infra que el reto pide NO están hechas.
- Después seguí al PASO 5 (ZIP).

Si es un proyecto REAL (manifiesto + código que compila o arranca):
- Seguí PASO 1 en adelante. 🔴 compilación sí. 🟡 pedagógico no.

PASO 1 — Detección y extracción
Identifica todos los archivos presentes en la cadena. Para cada archivo extrae:

Su ruta completa (ej: src/main/java/com/pragma/Service.java)
Su contenido o descripción

PASO 2 — Clasificación por tipo
Clasifica cada archivo en una de estas categorías:
A) Código fuente (Java, Python, TypeScript, JavaScript, Kotlin, etc.)
B) Configuración / documentación (YAML, properties, Markdown, JSON, txt, etc.)
C) Excel (.xlsx, .xls, .csv)
D) Word (.docx, .doc)
E) Otro tipo de archivo binario o especial
PASO 3 — Clasificación de errores en código fuente

Objetivo prioritario: que el proyecto compile. No corrijas flujo de negocio ni lógica funcional.

Antes de modificar cualquier archivo de código fuente, clasifica cada problema encontrado en una de estas dos categorías:
🔴 ERROR DE COMPILACIÓN — corregir siempre
Son errores que impiden que el proyecto arranque, sin valor pedagógico:

Import faltante o incorrecto
Clase, método o variable referenciada que no existe en ningún archivo del proyecto
Error de sintaxis
Anotación con atributos inválidos
Dependencia ausente en pom.xml, package.json, etc.
Archivo referenciado que no existe y debe ser creado con implementación mínima

→ CORREGIR estos errores.
🟡 PROBLEMA FUNCIONAL O DE CALIDAD — preservar siempre
Son problemas que no impiden compilar. Pueden ser intencionales para el aprendizaje:

Clave secreta hardcodeada ("secret", "password123")
API deprecada que funciona pero tiene reemplazo moderno
Lógica de negocio incorrecta o incompleta
Código redundante o de baja legibilidad
Falta de validaciones en flujo de negocio
Patrones de diseño incorrectos pero funcionales
Concurrencia no segura
Configuración funcional pero no óptima

→ PRESERVAR tal cual. No corregir, no mejorar, no comentar.
PASO 4 — Procesamiento según tipo de archivo
Tipo A — Código fuente
Aplica únicamente las correcciones clasificadas como 🔴 ERROR DE COMPILACIÓN.
No alteres ningún elemento clasificado como 🟡 PROBLEMA FUNCIONAL O DE CALIDAD.
Si falta un archivo referenciado, créalo con la implementación mínima necesaria para compilar.
Tipo B — Configuración / documentación
Extrae el contenido tal cual, sin modificaciones salvo errores evidentes de sintaxis
(ej: YAML mal indentado).
Tipo C — Excel (.xlsx)
Si viene con contenido real, genera el archivo respetando ese contenido.
Si viene con descripción en lenguaje natural, genera un archivo Excel funcional con:

Fila de encabezados en negrita con color de fondo distintivo
Columnas con ancho ajustado al contenido
Tipos de dato correctos por columna
Validaciones si la descripción lo indica
Hojas nombradas descriptivamente si hay más de una
Filas de ejemplo si no hay datos reales

Tipo D — Word (.docx)
Si viene con contenido real, genera el archivo respetando ese contenido.
Si viene con descripción en lenguaje natural, genera un documento Word funcional con:

Estilos de título (Título 1, Título 2) para jerarquía de secciones
Fuente legible (Calibri o equivalente), tamaño 11-12pt para cuerpo
Márgenes estándar
Tabla de contenido si tiene múltiples secciones
Tablas con encabezados en negrita si aplica

Tipo E — Otro
Genera el archivo con el contenido o estructura más apropiada según la descripción.
PASO 5 — Exportación en ZIP
Empaqueta todos los archivos en un único archivo ZIP descargable respetando exactamente
la estructura de rutas indicada por los marcadores.
El ZIP debe incluir:

Archivos de código con únicamente los errores de compilación corregidos
Archivos de configuración y documentación sin cambios
Archivos nuevos creados para resolver dependencias de compilación faltantes
Archivos Excel y Word generados desde descripción

IMPORTANTE: El ZIP debe estar listo para descargar al finalizar. No preguntes si el usuario
quiere generarlo. Simplemente genera el archivo y proporciona el enlace de descarga; No debes desplegar en el chat el resumen de lo que arreglaste al Zip, solo entregalo.

REGLAS IMPORTANTES

No omitas ningún archivo aunque no tenga errores ni modificaciones
Respeta los nombres y rutas exactas indicadas por los marcadores
Si un archivo no tiene marcador claro, infiere el nombre desde su contenido
Si la cadena contiene solo documentación, placeholders o binarios fake, NO la reproduzcas:
aplicá PASO 0 (materializar el proyecto del briefing). Reproducir la carcasa es un fallo.
No agregues texto después del enlace de descarga del ZIP
No preguntes si el usuario quiere el ZIP: simplemente generalo siempre
Si detectas que falta un archivo de configuración necesario para compilar
(pom.xml, package.json, requirements.txt, build.gradle, etc.), créalo e inclúyelo
inferiendo su contenido desde los imports y frameworks detectados en el código
Nunca corrijas problemas 🟡 aunque parezcan obvios o fáciles de mejorar.
El participante que recibirá este proyecto los debe encontrar y resolver él mismo.


INPUT
Aquí está la cadena con los archivos:

// === ARCHIVO: pyproject.toml ===
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "pragma-normativa-rag"
version = "0.1.0"
description = "Sistema de consulta normativa con modelos generativos y RAG"
readme = "README.md"
requires-python = ">=3.13"
license = {text = "MIT"}
authors = [
    {name = "PragmaFintech Team", email = "team@pragmafintech.com"}
]
keywords = ["rag", "llm", "bedrock", "fastapi", "normativa"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.13",
    "Framework :: FastAPI",
]

dependencies = [
    "fastapi==0.115.0",
    "uvicorn==0.30.1",
    "pydantic==2.9.0",
    "pydantic-settings==2.4.0",
    "langchain==0.2.5",
    "langchain-aws==0.1.6",
    "langchain-community==0.2.5",
    "boto3==1.34.120",
    "botocore==1.34.120",
    "python-dotenv==1.0.1",
    "python-multipart==0.0.9",
    "aiohttp==3.10.0",
    "tenacity==8.3.0",
    "httpx==0.27.0",
]

[project.optional-dependencies]
dev = [
    "pytest==8.2.0",
    "pytest-asyncio==0.23.7",
    "pytest-cov==5.0.0",
    "ruff==0.5.0",
    "mypy==1.10.0",
    "black==24.4.2",
    "pre-commit==3.7.1",
]

[project.urls]
Homepage = "https://github.com/pragmafintech/normativa-rag"
Documentation = "https://docs.pragmafintech.com/normativa-rag"
Repository = "https://github.com/pragmafintech/normativa-rag"

[tool.setuptools.packages.find]
where = ["."]
include = ["app*", "infra*"]

[tool.ruff]
line-length = 100
target-version = "py313"
select = [
    "E",
    "F",
    "W",
    "I",
    "N",
    "UP",
    "ANN",
    "B",
    "A",
    "C4",
]
ignore = [
    "ANN101",
    "ANN102",
    "ANN401",
]

[tool.ruff.per-file-ignores]
"__init__.py" = ["F401"]
"tests/*" = ["ANN", "B011"]

[tool.mypy]
python_version = "3.13"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false
disallow_incomplete_defs = true
check_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
strict_equality = true

[[tool.mypy.overrides]]
module = ["boto3.*", "botocore.*"]
ignore_missing_imports = true

[[tool.mypy.overrides]]
module = ["pytest.*"]
ignore_missing_imports = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
asyncio_mode = "auto"
addopts = "-v --tb=short --strict-markers"
markers = [
    "unit: Unit tests",
    "integration: Integration tests",
    "slow: Slow running tests",
]

// === ARCHIVO: app/main.py ===
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

// === ARCHIVO: app/config/settings.py ===
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


// === ARCHIVO: infra/terraform/variables.tf ===
variable "aws_region" {
  description = "Región de AWS donde se desplegarán los recursos"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Entorno de despliegue (development, staging, production)"
  type        = string
  default     = "development"
  validation {
    condition     = contains(["development", "staging", "production"], var.environment)
    error_message = "El entorno debe ser development, staging o production."
  }
}

variable "project_name" {
  description = "Nombre del proyecto para identificar recursos"
  type        = string
  default     = "pragma-normativa-rag"
}

variable "vpc_cidr" {
  description = "CIDR block para la VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "Zonas de disponibilidad para los recursos"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks para subredes públicas"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks para subredes privadas"
  type        = list(string)
  default     = ["10.0.11.0/24", "10.0.12.0/24"]
}

variable "lambda_memory_size" {
  description = "Memoria en MB para la función Lambda"
  type        = number
  default     = 512
}

variable "lambda_timeout" {
  description = "Timeout en segundos para la función Lambda"
  type        = number
  default     = 300
}

variable "lambda_runtime" {
  description = "Runtime de Python para Lambda"
  type        = string
  default     = "python3.13"
}

variable "bedrock_model_id" {
  description = "ID del modelo de Bedrock a utilizar"
  type        = string
  default     = "anthropic.claude-3-sonnet-20240229-v1:0"
}

variable "pinecone_api_key" {
  description = "API Key de Pinecone para almacenamiento vectorial"
  type        = string
  sensitive   = true
  default     = ""
}

variable "pinecone_environment" {
  description = "Entorno de Pinecone"
  type        = string
  default     = ""
}

variable "qdrant_url" {
  description = "URL del servicio Qdrant"
  type        = string
  default     = ""
}

variable "qdrant_api_key" {
  description = "API Key de Qdrant"
  type        = string
  sensitive   = true
  default     = ""
}

variable "allowed_cors_origins" {
  description = "Orígenes permitidos para CORS"
  type        = list(string)
  default     = ["http://localhost:3000", "http://localhost:8000"]
}

variable "log_level" {
  description = "Nivel de logging para la aplicación"
  type        = string
  default     = "INFO"
  validation {
    condition     = contains(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], var.log_level)
    error_message = "El nivel de logging debe ser DEBUG, INFO, WARNING, ERROR o CRITICAL."
  }
}

variable "rate_limit_per_minute" {
  description = "Límite de requests por minuto"
  type        = number
  default     = 60
}

variable "enable_dynamodb" {
  description = "Habilitar DynamoDB para almacenamiento de logs"
  type        = bool
  default     = true
}

variable "dynamodb_billing_mode" {
  description = "Modo de facturación de DynamoDB"
  type        = string
  default     = "PAY_PER_REQUEST"
  validation {
    condition     = contains(["PAY_PER_REQUEST", "PROVISIONED"], var.dynamodb_billing_mode)
    error_message = "El modo de facturación debe ser PAY_PER_REQUEST o PROVISIONED."
  }
}

variable "enable_api_gateway_auth" {
  description = "Habilitar autenticación en API Gateway"
  type        = bool
  default     = false
}

variable "api_gateway_usage_plan_quota" {
  description = "Cuota de requests para el usage plan"
  type        = number
  default     = 10000
}

variable "additional_tags" {
  description = "Tags adicionales para todos los recursos"
  type        = map(string)
  default     = {}
}

// === ARCHIVO: app/models/bedrock.py ===
import logging
import time
from dataclasses import dataclass
from typing import Any, Literal

import boto3
from botocore.exceptions import ClientError, BotoCoreError

from app.config.settings import get_settings
from app.utils.exceptions import BedrockInvocationError


logger = get_logger(__name__)


@dataclass
class BedrockResponse:
    text: str
    model_id: str
    input_tokens: int
    output_tokens: int
    latency_ms: float
    stop_reason: str | None = None


@dataclass
class BedrockError:
    error_type: Literal[
        "ModelTimeoutException",
        "ModelNotFoundException",
        "AccessDeniedException",
        "ThrottlingException",
        "InternalServerException",
        "ValidationException",
        "Unknown",
    ]
    message: str
    retryable: bool


class BedrockClient:
    def __init__(self) -> None:
        settings = get_settings()
        self.model_id = settings.bedrock_model_id
        self.max_tokens = settings.bedrock_max_tokens
        self.temperature = settings.bedrock_temperature
        self.top_p = settings.bedrock_top_p
        self.aws_region = settings.aws_region

        self.client = boto3.client(
            "bedrock-runtime",
            region_name=self.aws_region,
        )
        logger.info(
            "BedrockClient inicializado",
            extra={
                "model_id": self.model_id,
                "region": self.aws_region,
                "max_tokens": self.max_tokens,
            },
        )

    def invoke_model(
        self,
        prompt: str,
        system_prompt: str | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
    ) -> BedrockResponse:
        start_time = time.perf_counter()

        body = self._build_request_body(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=max_tokens or self.max_tokens,
            temperature=temperature if temperature is not None else self.temperature,
            top_p=top_p if top_p is not None else self.top_p,
        )

        try:
            logger.debug(
                "Invocando modelo Bedrock",
                extra={
                    "model_id": self.model_id,
                    "prompt_length": len(prompt),
                    "max_tokens": max_tokens or self.max_tokens,
                },
            )

            response = self.client.invoke_model(
                modelId=self.model_id,
                body=body,
                accept="application/json",
                contentType="application/json",
            )

            response_body = response["body"].read().decode("utf-8")
            result = self._parse_response(response_body)

            latency_ms = (time.perf_counter() - start_time) * 1000

            logger.info(
                "Modelo Bedrock invocado exitosamente",
                extra={
                    "model_id": self.model_id,
                    "input_tokens": result.input_tokens,
                    "output_tokens": result.output_tokens,
                    "latency_ms": round(latency_ms, 2),
                    "stop_reason": result.stop_reason,
                },
            )

            result.latency_ms = latency_ms
            return result

        except ClientError as exc:
            error = self._classify_error(exc)
            logger.error(
                "Error de cliente al invocar Bedrock",
                extra={
                    "error_type": error.error_type,
                    "error_message": error.message,
                    "retryable": error.retryable,
                },
            )
            raise BedrockInvocationError(
                message=error.message,
                error_type=error.error_type,
                retryable=error.retryable,
            ) from exc

        except BotoCoreError as exc:
            logger.error(
                "Error de conexión con Bedrock",
                extra={"error_message": str(exc)},
            )
            raise BedrockInvocationError(
                message=f"Error de conexión: {str(exc)}",
                error_type="ModelTimeoutException",
                retryable=True,
            ) from exc

        except Exception as exc:
            logger.critical(
                "Error inesperado al invocar Bedrock",
                extra={"error_type": type(exc).__name__},
                exc_info=True,
            )
            raise BedrockInvocationError(
                message=f"Error inesperado: {str(exc)}",
                error_type="Unknown",
                retryable=False,
            ) from exc

    def _build_request_body(
        self,
        prompt: str,
        system_prompt: str | None,
        max_tokens: int,
        temperature: float,
        top_p: float,
    ) -> str:
        if "claude" in self.model_id.lower():
            messages = []
            if system_prompt:
                messages.append({
                    "role": "user",
                    "content": f"\n\nHuman: {system_prompt}\n\nAssistant:",
                })
            messages.append({
                "role": "user",
                "content": f"{prompt}",
            })

            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "messages": messages,
                "temperature": temperature,
                "top_p": top_p,
            }
            return str(body).replace("'", '"')

        elif "mistral" in self.model_id.lower():
            body = {
                "prompt": f"<s>[INST] {prompt} [/INST]",
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": top_p,
            }
            return str(body).replace("'", '"')

        else:
            body = {
                "inputText": prompt,
                "textGenerationConfig": {
                    "maxTokenCount": max_tokens,
                    "temperature": temperature,
                    "topP": top_p,
                },
            }
            return str(body).replace("'", '"')

    def _parse_response(self, response_body: str) -> BedrockResponse:
        import json
        data = json.loads(response_body)

        if "claude" in self.model_id.lower():
            content = data.get("content", [])
            text = content[0]["text"] if content else ""
            usage = data.get("usage", {})
            return BedrockResponse(
                text=text,
                model_id=self.model_id,
                input_tokens=usage.get("input_tokens", 0),
                output_tokens=usage.get("output_tokens", 0),
                latency_ms=0.0,
                stop_reason=data.get("stop_reason"),
            )

        elif "mistral" in self.model_id.lower():
            outputs = data.get("outputs", [])
            text = outputs[0]["text"] if outputs else ""
            return BedrockResponse(
                text=text,
                model_id=self.model_id,
                input_tokens=data.get("prompt_tokens", 0),
                output_tokens=data.get("tokens", 0),
                latency_ms=0.0,
                stop_reason=None,
            )

        else:
            results = data.get("results", [])
            text = results[0]["outputText"] if results else ""
            return BedrockResponse(
                text=text,
                model_id=self.model_id,
                input_tokens=data.get("inputTextTokenCount", 0),
                output_tokens=data.get("resultTokenCount", 0),
                latency_ms=0.0,
                stop_reason=None,
            )

    def _classify_error(self, exc: ClientError) -> BedrockError:
        error_code = exc.response.get("Error", {}).get("Code", "Unknown")
        error_message = exc.response.get("Error", {}).get("Message", str(exc))

        error_mapping: dict[str, tuple[str, bool]] = {
            "ModelTimeoutException": ("ModelTimeoutException", True),
            "ModelNotFoundException": ("ModelNotFoundException", False),
            "AccessDeniedException": ("AccessDeniedException", False),
            "ThrottlingException": ("ThrottlingException", True),
            "InternalServerException": ("InternalServerException", True),
            "ValidationException": ("ValidationException", False),
            "ResourceNotFoundException": ("ModelNotFoundException", False),
        }

        error_type, retryable = error_mapping.get(
            error_code,
            ("Unknown", error_code in ["ThrottlingException", "ModelTimeoutException"],
        )

        return BedrockError(
            error_type=error_type,
            message=error_message,
            retryable=retryable,
        )

    def check_model_availability(self) -> bool:
        try:
            self.client.list_foundation_models()
            logger.info("Modelo Bedrock disponible")
            return True
        except Exception as exc:
            logger.warning(
                "Modelo Bedrock no disponible",
                extra={"error": str(exc)},
            )
            return False


bedrock_client = BedrockClient()


// === ARCHIVO: app/api/schemas.py ===
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

// === ARCHIVO: app/api/endpoints.py ===
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

// === ARCHIVO: app/prompts/templates.py ===
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


// === ARCHIVO: app/retrieval/vector_store.py ===
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


// === ARCHIVO: app/chains/orchestrator.py ===
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


// === ARCHIVO: app/eval/evaluation.py ===
"""Conjunto de evaluación con métricas reproducibles para el sistema de consulta normativa."""

from dataclasses import dataclass
from typing import Any

from app.eval.metrics import (
    AnswerRelevanceMetric,
    CosineSimilarityMetric,
    FaithfulnessMetric,
    MetricResult,
)


@dataclass
class EvaluationCase:
    """Caso de prueba para evaluación del sistema RAG."""
    query: str
    expected_themes: list[str]
    min_relevance_score: float
    min_faithfulness_score: float
    ground_truth_answer: str | None = None


@dataclass
class EvaluationReport:
    """Reporte consolidado de evaluación del sistema."""
    total_cases: int
    passed_cases: int
    average_relevance: float
    average_faithfulness: float
    average_cosine_similarity: float
    failed_queries: list[str]
    metrics_by_case: dict[str, dict[str, float]]


class EvaluationSuite:
    """Suite de evaluación con casos de prueba deterministas."""

    def __init__(
        self,
        relevance_metric: AnswerRelevanceMetric,
        faithfulness_metric: FaithfulnessMetric,
        similarity_metric: CosineSimilarityMetric,
    ) -> None:
        self.relevance_metric = relevance_metric
        self.faithfulness_metric = faithfulness_metric
        self.similarity_metric = similarity_metric
        self.test_cases = self._load_test_cases()

    def _load_test_cases(self) -> list[EvaluationCase]:
        """Carga casos de prueba predefinidos para evaluación."""
        return [
            EvaluationCase(
                query="¿Cuál es el procedimiento para solicitar vacaciones?",
                expected_themes=["vacaciones", "solicitud", "procedimiento", "política"],
                min_relevance_score=0.7,
                min_faithfulness_score=0.8,
                ground_truth_answer="El empleado debe presentar la solicitud con 15 días de anticipación...",
            ),
            EvaluationCase(
                query="¿Qué cubre el seguro de gastos médicos?",
                expected_themes=["seguro", "gastos médicos", "cobertura", "beneficios"],
                min_relevance_score=0.7,
                min_faithfulness_score=0.75,
                ground_truth_answer="El seguro cubre hospitalización, consultas y medicamentos...",
            ),
            EvaluationCase(
                query="¿Cómo funciona el plan de retiro?",
                expected_themes=["retiro", "pensión", "ahorro", "jubilación"],
                min_relevance_score=0.65,
                min_faithfulness_score=0.7,
                ground_truth_answer="El plan de retiro incluye aportaciones patronales y del empleado...",
            ),
            EvaluationCase(
                query="¿Cuáles son las políticas de uso de vehículos corporativos?",
                expected_themes=["vehículo", "corporativo", "uso", "política", "combustible"],
                min_relevance_score=0.7,
                min_faithfulness_score=0.8,
            ),
            EvaluationCase(
                query="¿Qué hacer en caso de emergencia en oficina?",
                expected_themes=["emergencia", "evacuación", "seguridad", "protocolo"],
                min_relevance_score=0.75,
                min_faithfulness_score=0.85,
            ),
            EvaluationCase(
                query="¿Cuál es el proceso de evaluación de desempeño?",
                expected_themes=["evaluación", "desempeño", "metas", "feedback"],
                min_relevance_score=0.7,
                min_faithfulness_score=0.75,
            ),
            EvaluationCase(
                query="¿Cómo solicito un reembolso de gastos?",
                expected_themes=["reembolso", "gastos", "solicitud", "viáticos"],
                min_relevance_score=0.7,
                min_faithfulness_score=0.8,
            ),
            EvaluationCase(
                query="¿Qué beneficios ofrece el programa de bienestar?",
                expected_themes=["bienestar", "beneficios", "salud", "programa"],
                min_relevance_score=0.65,
                min_faithfulness_score=0.7,
            ),
        ]

    def evaluate_response(
        self,
        query: str,
        response: str,
        retrieved_context: list[str],
        expected_themes: list[str],
    ) -> dict[str, MetricResult]:
        """Evalúa una respuesta del sistema RAG."""
        relevance_result = self.relevance_metric.compute(
            query=query,
            response=response,
            expected_themes=expected_themes,
        )

        faithfulness_result = self.faithfulness_metric.compute(
            response=response,
            retrieved_context=retrieved_context,
        )

        similarity_result = self.similarity_metric.compute(
            response=response,
            reference_texts=retrieved_context,
        )

        return {
            "relevance": relevance_result,
            "faithfulness": faithfulness_result,
            "cosine_similarity": similarity_result,
        }

    def run_full_evaluation(
        self,
        system_response_fn: Any,
    ) -> EvaluationReport:
        """Ejecuta la evaluación completa sobre todos los casos de prueba."""
        metrics_by_case: dict[str, dict[str, float]] = {}
        failed_queries: list[str] = []
        total_relevance = 0.0
        total_faithfulness = 0.0
        total_similarity = 0.0

        for case in self.test_cases:
            try:
                result = system_response_fn(case.query)
                response = result.get("response", "")
                context = result.get("context", [])

                metrics = self.evaluate_response(
                    query=case.query,
                    response=response,
                    retrieved_context=context,
                    expected_themes=case.expected_themes,
                )

                relevance_score = metrics["relevance"].score
                faithfulness_score = metrics["faithfulness"].score
                similarity_score = metrics["cosine_similarity"].score

                metrics_by_case[case.query] = {
                    "relevance": relevance_score,
                    "faithfulness": faithfulness_score,
                    "cosine_similarity": similarity_score,
                }

                total_relevance += relevance_score
                total_faithfulness += faithfulness_score
                total_similarity += similarity_score

                if relevance_score < case.min_relevance_score:
                    failed_queries.append(case.query)
                elif faithfulness_score < case.min_faithfulness_score:
                    failed_queries.append(case.query)

            except Exception as e:
                failed_queries.append(case.query)
                metrics_by_case[case.query] = {
                    "relevance": 0.0,
                    "faithfulness": 0.0,
                    "cosine_similarity": 0.0,
                    "error": str(e),
                }

        total_cases = len(self.test_cases)
        return EvaluationReport(
            total_cases=total_cases,
            passed_cases=total_cases - len(failed_queries),
            average_relevance=total_relevance / total_cases,
            average_faithfulness=total_faithfulness / total_cases,
            average_cosine_similarity=total_similarity / total_cases,
            failed_queries=failed_queries,
            metrics_by_case=metrics_by_case,
        )


def create_evaluation_suite() -> EvaluationSuite:
    """Crea una instancia de la suite de evaluación con métricas por defecto."""
    relevance = AnswerRelevanceMetric()
    faithfulness = FaithfulnessMetric()
    similarity = CosineSimilarityMetric()

    return EvaluationSuite(
        relevance_metric=relevance,
        faithfulness_metric=faithfulness,
        similarity_metric=similarity,
    )


// === ARCHIVO: app/eval/metrics.py ===
"""Definición de métricas personalizadas para evaluar la calidad de las respuestas del sistema RAG."""

from dataclasses import dataclass
from math import sqrt
from typing import Any


@dataclass
class MetricResult:
    """Resultado de una métrica de evaluación."""
    score: float
    details: dict[str, Any]


class BaseMetric:
    """Clase base para métricas de evaluación."""

    def compute(self, **kwargs: Any) -> MetricResult:
        """Método abstracto para calcular la métrica."""
        raise NotImplementedError

    def _normalize_score(self, score: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
        """Normaliza un score al rango [0, 1]."""
        if max_val == min_val:
            return 1.0
        normalized = (score - min_val) / (max_val - min_val)
        return max(0.0, min(1.0, normalized))


class CosineSimilarityMetric(BaseMetric):
    """Calcula similitud coseno entre la respuesta y el contexto recuperado."""

    def compute(self, response: str, reference_texts: list[str]) -> MetricResult:
        """Calcula la similitud coseno usando embedding simple por palabras."""
        response_tokens = self._tokenize(response.lower())

        if not response_tokens or not reference_texts:
            return MetricResult(
                score=0.0,
                details={"reason": "Sin contenido para comparar"},
            )

        similarities: list[float] = []
        for ref_text in reference_texts:
            ref_tokens = self._tokenize(ref_text.lower())
            similarity = self._cosine_similarity(response_tokens, ref_tokens)
            similarities.append(similarity)

        avg_similarity = sum(similarities) / len(similarities) if similarities else 0.0

        return MetricResult(
            score=self._normalize_score(avg_similarity),
            details={
                "max_similarity": max(similarities) if similarities else 0.0,
                "min_similarity": min(similarities) if similarities else 0.0,
                "response_token_count": len(response_tokens),
            },
        )

    def _tokenize(self, text: str) -> dict[str, int]:
        """Convierte texto a mapa de frecuencia de tokens."""
        tokens = text.split()
        frequency: dict[str, int] = {}
        for token in tokens:
            if len(token) > 2:
                frequency[token] = frequency.get(token, 0) + 1
        return frequency

    def _cosine_similarity(
        self,
        vec1: dict[str, int],
        vec2: dict[str, int],
    ) -> float:
        """Calcula similitud coseno entre dos vectores de frecuencia."""
        all_tokens = set(vec1.keys()) | set(vec2.keys())

        dot_product = sum(vec1.get(t, 0) * vec2.get(t, 0) for t in all_tokens)
        magnitude1 = sqrt(sum(v**2 for v in vec1.values()))
        magnitude2 = sqrt(sum(v**2 for v in vec2.values()))

        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0

        return dot_product / (magnitude1 * magnitude2)


class AnswerRelevanceMetric(BaseMetric):
    """Mide la relevancia de la respuesta respecto a los temas esperados."""

    def compute(
        self,
        query: str,
        response: str,
        expected_themes: list[str],
    ) -> MetricResult:
        """Calcula cuántos temas esperados aparecen en la respuesta."""
        response_lower = response.lower()
        query_lower = query.lower()

        matched_themes: list[str] = []
        partial_matches: list[str] = []

        for theme in expected_themes:
            theme_lower = theme.lower()
            if theme_lower in response_lower:
                matched_themes.append(theme)
            elif any(word in response_lower for word in theme_lower.split()):
                partial_matches.append(theme)

        theme_coverage = len(matched_themes) / len(expected_themes) if expected_themes else 0.0
        partial_bonus = len(partial_matches) * 0.1 / len(expected_themes) if expected_themes else 0.0

        query_in_response = 1.0 if query_lower[:30] in response_lower else 0.0

        final_score = min(1.0, theme_coverage + partial_bonus + query_in_response * 0.2)

        return MetricResult(
            score=self._normalize_score(final_score),
            details={
                "matched_themes": matched_themes,
                "partial_matches": partial_matches,
                "theme_coverage": theme_coverage,
                "query_mentioned": query_in_response > 0,
            },
        )


class FaithfulnessMetric(BaseMetric):
    """Evalúa si la respuesta es fiel al contexto recuperado."""

    def compute(
        self,
        response: str,
        retrieved_context: list[str],
    ) -> MetricResult:
        """Verifica que la respuesta no contradiga el contexto recuperado."""
        if not retrieved_context:
            return MetricResult(
                score=0.0,
                details={"reason": "Sin contexto recuperado"},
            )

        response_lower = response.lower()
        context_combined = " ".join(retrieved_context).lower()

        response_sentences = self._split_sentences(response_lower)
        context_sentences = self._split_sentences(context_combined)

        contradictions = 0
        supported_statements = 0

        for resp_sent in response_sentences:
            if len(resp_sent) < 10:
                continue

            has_support = False
            for ctx_sent in context_sentences:
                if len(ctx_sent) < 10:
                    continue
                if self._sentence_overlap(resp_sent, ctx_sent) > 0.4:
                    has_support = True
                    break

            if has_support:
                supported_statements += 1

        total_statements = len(response_sentences)
        if total_statements == 0:
            faithfulness = 0.5
        else:
            faithfulness = supported_statements / total_statements

        return MetricResult(
            score=self._normalize_score(faithfulness),
            details={
                "supported_statements": supported_statements,
                "total_statements": total_statements,
                "contradictions": contradictions,
            },
        )

    def _split_sentences(self, text: str) -> list[str]:
        """Divide texto en oraciones."""
        import re
        sentences = re.split(r"[.!?]+", text)
        return [s.strip() for s in sentences if s.strip()]

    def _sentence_overlap(self, sent1: str, sent2: str) -> float:
        """Calcula overlap entre dos oraciones."""
        words1 = set(sent1.split())
        words2 = set(sent2.split())

        if not words1 or not words2:
            return 0.0

        intersection = words1 & words2
        union = words1 | words2

        return len(intersection) / len(union) if union else 0.0


class HumanEvaluationSimulator(BaseMetric):
    """Simula evaluación humana con métricas proxy."""

    def compute(
        self,
        response: str,
        query: str,
        reference_answer: str | None = None,
    ) -> MetricResult:
        """Simula evaluación humana basada en criterios proxies."""
        response_words = response.split()

        length_score = self._evaluate_length(response_words)
        clarity_score = self._evaluate_clarity(response)
        completeness_score = self._evaluate_completeness(response, query)

        if reference_answer:
            ref_similarity = CosineSimilarityMetric().compute(
                response, [reference_answer]
            )
            final_score = (
                length_score * 0.2
                + clarity_score * 0.3
                + completeness_score * 0.2
                + ref_similarity.score * 0.3
            )
        else:
            final_score = (length_score * 0.3 + clarity_score * 0.4 + completeness_score * 0.3)

        return MetricResult(
            score=self._normalize_score(final_score),
            details={
                "length_score": length_score,
                "clarity_score": clarity_score,
                "completeness_score": completeness_score,
            },
        )

    def _evaluate_length(self, words: list[str]) -> float:
        """Evalúa si la longitud de la respuesta es apropiada."""
        word_count = len(words)
        if 20 <= word_count <= 200:
            return 1.0
        elif word_count < 20:
            return word_count / 20.0
        else:
            return max(0.0, 1.0 - (word_count - 200) / 300.0)

    def _evaluate_clarity(self, response: str) -> float:
        """Evalúa claridad basada en estructura y formato."""
        has_structure = any(marker in response for marker in [".", "•", "-", ":"])
        has_numbers = any(char.isdigit() for char in response)
        avg_word_length = sum(len(w) for w in response.split()) / len(response.split()) if response.split() else 0

        score = 0.0
        if has_structure:
            score += 0.4
        if has_numbers:
            score += 0.3
        if 4 <= avg_word_length <= 8:
            score += 0.3

        return score

    def _evaluate_completeness(self, response: str, query: str) -> float:
        """Evalúa si la respuesta responde todos los aspectos de la pregunta."""
        query_lower = query.lower()
        response_lower = response.lower()

        question_words = set(query_lower.split())
        answer_words = set(response_lower.split())

        overlap = question_words & answer_words
        coverage = len(overlap) / len(question_words) if question_words else 0.0

        has_answer = any(
            indicator in response_lower
            for indicator in ["es", "son", "es posible", "se puede", "el", "la", "los", "las"]
        )

        return coverage * 0.6 + (0.4 if has_answer else 0.0)


=== ARCHIVO: app/utils/logging.py ===
"""Configuración de logging estructurado para observabilidad del sistema RAG."""

import logging
import sys
import time
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any
from functools import wraps


class StructuredFormatter(logging.Formatter):
    """Formateador que genera logs estructurados en formato JSON."""

    def format(self, record: logging.LogRecord) -> str:
        import json

        log_entry = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        if hasattr(record, "extra_fields"):
            log_entry.update(record.extra_fields)

        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry)


class LatencyTracker:
    """Tracker para métricas de latencia de operaciones."""

    def __init__(self, operation_name: str, logger: logging.Logger) -> None:
        self.operation_name = operation_name
        self.logger = logger
        self.start_time: float = 0.0
        self.end_time: float = 0.0

    def __enter__(self) -> "LatencyTracker":
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.end_time = time.perf_counter()
        latency_ms = (self.end_time - self.start_time) * 1000

        extra_fields = {
            "operation": self.operation_name,
            "latency_ms": round(latency_ms, 2),
            "success": exc_type is None,
        }

        if exc_type is not None:
            extra_fields["error"] = exc_type.__name__

        self.logger.info(
            f"Operation {self.operation_name} completed",
            extra={"extra_fields": extra_fields},
        )


class TokenTracker:
    """Tracker para métricas de consumo de tokens."""

    def __init__(self, logger: logging.Logger) -> None:
        self.logger = logger
        self.input_tokens: int = 0
        self.output_tokens: int = 0
        self.total_tokens: int = 0

    def record_tokens(
        self,
        input_tokens: int,
        output_tokens: int,
        model_id: str,
        cost_per_token: float = 0.0,
    ) -> None:
        """Registra el consumo de tokens y calcula el costo estimado."""
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
        self.total_tokens = input_tokens + output_tokens

        estimated_cost = self.total_tokens * cost_per_token

        extra_fields = {
            "model_id": model_id,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": self.total_tokens,
            "estimated_cost_usd": round(estimated_cost, 6),
        }

        self.logger.info(
            f"Token usage for model {model_id}",
            extra={"extra_fields": extra_fields},
        )

    def get_summary(self) -> dict[str, Any]:
        """Retorna un resumen del consumo de tokens."""
        return {
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "total_tokens": self.total_tokens,
        }


def setup_logging(log_level: str = "INFO") -> None:
    """Configura el sistema de logging con formateador estructurado."""
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    if root_logger.handlers:
        root_logger.handlers.clear()

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(StructuredFormatter())

    root_logger.addHandler(console_handler)

    for logger_name in ["app", "uvicorn", "httpx"]:
        logger = logging.getLogger(logger_name)
        logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))


def get_logger(name: str) -> logging.Logger:
    """Obtiene un logger configurado para el módulo especificado."""
    return logging.getLogger(name)


@asynccontextmanager
async def log_async_operation(operation_name: str, logger: logging.Logger, **kwargs: Any):
    """Context manager para registrar operaciones asíncronas con latencia."""
    start_time = time.perf_counter()
    extra_fields = {"operation": operation_name, **kwargs}

    logger.info(f"Starting {operation_name}", extra={"extra_fields": extra_fields})

    try:
        yield
        end_time = time.perf_counter()
        latency_ms = (end_time - start_time) * 1000

        success_fields = {
            **extra_fields,
            "latency_ms": round(latency_ms, 2),
            "success": True,
        }
        logger.info(f"Completed {operation_name}", extra={"extra_fields": success_fields})

    except Exception as exc:
        end_time = time.perf_counter()
        latency_ms = (end_time - start_time) * 1000

        error_fields = {
            **extra_fields,
            "latency_ms": round(latency_ms, 2),
            "success": False,
            "error_type": type(exc).__name__,
            "error_message": str(exc),
        }
        logger.error(f"Failed {operation_name}", extra={"extra_fields": error_fields})
        raise


def log_function_call(logger: logging.Logger) -> Any:
    """Decorador para registrar llamadas a funciones con sus argumentos."""

    def decorator(func: Any) -> Any:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            func_name = func.__name__
            extra_fields = {
                "function": func_name,
                "args_count": len(args),
                "kwargs_keys": list(kwargs.keys()),
            }

            logger.debug(f"Calling {func_name}", extra={"extra_fields": extra_fields})

            try:
                result = func(*args, **kwargs)
                logger.debug(f"Completed {func_name}", extra={"extra_fields": {"function": func_name}})
                return result
            except Exception as exc:
                error_fields = {
                    **extra_fields,
                    "error": type(exc).__name__,
                    "message": str(exc),
                }
                logger.error(f"Error in {func_name}", extra={"extra_fields": error_fields})
                raise

        return wrapper

    return decorator


// === ARCHIVO: app/utils/exceptions.py ===
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


// === ARCHIVO: data/sample_data.json ===
{
  "evaluation_cases": [
    {
      "case_id": "eval_001",
      "query": "¿Cuál es el procedimiento para solicitar vacaciones en PragmaFintech?",
      "expected_response_contains": ["vacaciones", "solicitud", "recursos humanos", "política"],
      "expected_context_sources": ["manual_empleado", "politica_vacaciones"],
      "difficulty": "easy",
      "category": "rrhh"
    },
    {
      "case_id": "eval_002",
      "query": "¿Qué hacer si detecto un problema de seguridad en los sistemas?",
      "expected_response_contains": ["seguridad", "reportar", "incidente", "equipo"],
      "expected_context_sources": ["politica_seguridad", "protocolo_incidentes"],
      "difficulty": "easy",
      "category": "seguridad"
    },
    {
      "case_id": "eval_003",
      "query": "¿Cuáles son los requisitos para solicitar un préstamo corporativo?",
      "expected_response_contains": ["préstamo", "corporativo", "requisitos", "aprobación"],
      "expected_context_sources": ["politica_financiera", "procedimiento_prestamos"],
      "difficulty": "medium",
      "category": "finanzas"
    },
    {
      "case_id": "eval_004",
      "query": "Explique el código de conducta ética de la empresa",
      "expected_response_contains": ["ética", "conducta", "conflicto", "interés"],
      "expected_context_sources": ["codigo_etica", "manual_cumplimiento"],
      "difficulty": "easy",
      "category": "cumplimiento"
    },
    {
      "case_id": "eval_005",
      "query": "¿Cuál es el proceso de onboarding para nuevos empleados?",
      "expected_response_contains": ["onboarding", "incorporación", "capacitación", "primer día"],
      "expected_context_sources": ["proceso_onboarding", "guia_bienvenida"],
      "difficulty": "easy",
      "category": "rrhh"
    },
    {
      "case_id": "eval_006",
      "query": "¿Qué beneficios tiene el plan de salud para empleados?",
      "expected_response_contains": ["beneficios", "salud", "plan", "cobertura"],
      "expected_context_sources": ["beneficios_empleado", "plan_salud"],
      "difficulty": "medium",
      "category": "rrhh"
    },
    {
      "case_id": "eval_007",
      "query": "¿Cómo reporto gastos de viaje para reembolso?",
      "expected_response_contains": ["gastos", "viaje", "reembolso", "aprobación"],
      "expected_context_sources": ["politica_gastos", "procedimiento_viajes"],
      "difficulty": "easy",
      "category": "finanzas"
    },
    {
      "case_id": "eval_008",
      "query": "¿Cuál es la política de trabajo remoto de la empresa?",
      "expected_response_contains": ["remoto", "teletrabajo", "presencial", "horario"],
      "expected_context_sources": ["politica_remoto", "manual_empleado"],
      "difficulty": "easy",
      "category": "rrhh"
    },
    {
      "case_id": "eval_009",
      "query": "¿Qué procedimientos debo seguir para una auditoría interna?",
      "expected_response_contains": ["auditoría", "interna", "procedimiento", "documentación"],
      "expected_context_sources": ["manual_auditoria", "politica_cumplimiento"],
      "difficulty": "hard",
      "category": "cumplimiento"
    },
    {
      "case_id": "eval_010",
      "query": "¿Cómo solicito una promoción o ascenso?",
      "expected_response_contains": ["promoción", "ascenso", "evaluación", "gerencia"],
      "expected_context_sources": ["politica_carrera", "procedimiento_promocion"],
      "difficulty": "medium",
      "category": "rrhh"
    }
  ],
  "test_documents": [
    {
      "doc_id": "manual_empleado",
      "title": "Manual del Empleado PragmaFintech",
      "content": "El manual del empleado contiene las políticas generales de la empresa, incluyendo normas de conducta, beneficios, y procedimientos administrativos. Todos los empleados deben leer y cumplir las políticas establecidas en este documento.",
      "category": "general"
    },
    {
      "doc_id": "politica_vacaciones",
      "title": "Política de Vacaciones",
      "content": "Los empleados tienen derecho a 20 días hábiles de vacaciones por año. La solicitud debe realizarse con al menos 15 días de anticipación a través del sistema de recursos humanos. La aprobación depende del gerente directo.",
      "category": "rrhh"
    },
    {
      "doc_id": "politica_seguridad",
      "title": "Política de Seguridad de la Información",
      "content": "Todo empleado tiene la obligación de reportar cualquier incidente de seguridad detectado en los sistemas. El reporte debe realizarse inmediatamente al equipo de seguridad informática mediante el formulario de incidentes.",
      "category": "seguridad"
    },
    {
      "doc_id": "politica_financiera",
      "title": "Política Financiera Corporativa",
      "content": "Los préstamos corporativos están disponibles para empleados con al menos un año de antigüedad. El monto máximo es equivalente a 6 meses de salario. Se requiere aprobación del área financiera y del gerente.",
      "category": "finanzas"
    },
    {
      "doc_id": "codigo_etica",
      "title": "Código de Ética",
      "content": "El código de ética de PragmaFintech establece los principios de integridad, honestidad y respeto. Los empleados deben evitar conflictos de interés y reportar cualquier situación que pueda comprometer la ética empresarial.",
      "category": "cumplimiento"
    }
  ],
  "evaluation_metrics": {
    "relevance": {
      "threshold": 0.7,
      "description": "Relevancia semántica entre la respuesta y la consulta"
    },
    "faithfulness": {
      "threshold": 0.8,
      "description": "Grado en que la respuesta se basa en el contexto recuperado"
    },
    "accuracy": {
      "threshold": 0.75,
      "description": "Precisión de la información proporcionada"
    },
    "completeness": {
      "threshold": 0.6,
      "description": "Grado en que la respuesta cubre todos los aspectos de la consulta"
    }
  },
  "query_patterns": {
    "informational": [
      "¿Qué es ...?",
      "¿Cuál es ...?",
      "¿Cómo funciona ...?",
      "Explique ..."
    ],
    "procedural": [
      "¿Cómo solicito ...?",
      "¿Cuál es el proceso para ...?",
      "¿Qué debo hacer para ...?",
      "¿Cuál es el procedimiento de ...?"
    ],
    "policy": [
      "¿Cuál es la política de ...?",
      "¿Qué dice la normativa sobre ...?",
      "¿Está permitido ...?",
      "¿Qué restricciones hay sobre ...?"
    ]
  }
}

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from httpx import AsyncClient, ASGITransport
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import create_app
from app.utils.exceptions import (
    InvalidQueryError,
    ContextRetrievalError,
    VectorStoreError,
    BedrockInvocationError,
)
from app.api.schemas import QueryRequest, QueryResponse


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
async def client(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.integration
class TestHealthEndpoint:
    async def test_health_check_returns_ok(self, client):
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "version" in data

    async def test_health_check_includes_timestamp(self, client):
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "timestamp" in data


@pytest.mark.integration
class TestQueryEndpoint:
    async def test_query_valid_request(self, client):
        payload = {"query": "¿Cuál es la política de vacaciones?"}
        with patch("app.api.endpoints.orchestrator") as mock_orch:
            mock_orch.arun = AsyncMock(
                return_value={
                    "answer": "La política de vacaciones establece 15 días hábiles anuales.",
                    "sources": ["normativa_2024.pdf"],
                    "confidence": 0.92,
                }
            )
            response = await client.post("/query", json=payload)
            assert response.status_code == 200
            data = response.json()
            assert "answer" in data
            assert "sources" in data
            assert "confidence" in data

    async def test_query_empty_query_returns_422(self, client):
        payload = {"query": ""}
        response = await client.post("/query", json=payload)
        assert response.status_code == 422

    async def test_query_missing_query_field_returns_422(self, client):
        payload = {}
        response = await client.post("/query", json=payload)
        assert response.status_code == 422

    async def test_query_too_short_query_returns_422(self, client):
        payload = {"query": "ab"}
        response = await client.post("/query", json=payload)
        assert response.status_code == 422

    async def test_query_invalid_query_error_handled(self, client):
        payload = {"query": "¿Cuál es la normativa?"}
        with patch("app.api.endpoints.orchestrator") as mock_orch:
            mock_orch.arun = AsyncMock(
                side_effect=InvalidQueryError("Query no válida para este contexto")
            )
            response = await client.post("/query", json=payload)
            assert response.status_code == 400
            data = response.json()
            assert "detail" in data

    async def test_query_context_retrieval_error_handled(self, client):
        payload = {"query": "¿Cuál es la política de gastos?"}
        with patch("app.api.endpoints.orchestrator") as mock_orch:
            mock_orch.arun = AsyncMock(
                side_effect=ContextRetrievalError("No se pudo recuperar contexto")
            )
            response = await client.post("/query", json=payload)
            assert response.status_code == 503
            data = response.json()
            assert "detail" in data

    async def test_query_vector_store_error_handled(self, client):
        payload = {"query": "¿Cuáles son los beneficios?"}
        with patch("app.api.endpoints.orchestrator") as mock_orch:
            mock_orch.arun = AsyncMock(
                side_effect=VectorStoreError("Error en la tienda de vectores")
            )
            response = await client.post("/query", json=payload)
            assert response.status_code == 500

    async def test_query_bedrock_error_handled(self, client):
        payload = {"query": "¿Qué dice la normativa de seguridad?"}
        with patch("app.api.endpoints.orchestrator") as mock_orch:
            mock_orch.arun = AsyncMock(
                side_effect=BedrockInvocationError("Timeout del modelo")
            )
            response = await client.post("/query", json=payload)
            assert response.status_code == 502

    async def test_query_unexpected_error_returns_500(self, client):
        payload = {"query": "¿Cuál es el procedimiento?"}
        with patch("app.api.endpoints.orchestrator") as mock_orch:
            mock_orch.arun = AsyncMock(side_effect=RuntimeError("Error inesperado"))
            response = await client.post("/query", json=payload)
            assert response.status_code == 500


@pytest.mark.integration
class TestQueryEndpointWithParameters:
    async def test_query_with_temperature_parameter(self, client):
        payload = {"query": "¿Política de remote work?", "temperature": 0.7}
        with patch("app.api.endpoints.orchestrator") as mock_orch:
            mock_orch.arun = AsyncMock(
                return_value={
                    "answer": "El trabajo remoto está permitido hasta 2 días por semana.",
                    "sources": ["normativa_laboral.pdf"],
                    "confidence": 0.88,
                }
            )
            response = await client.post("/query", json=payload)
            assert response.status_code == 200
            mock_orch.arun.assert_called_once()
            call_kwargs = mock_orch.arun.call_args.kwargs
            assert call_kwargs.get("temperature") == 0.7

    async def test_query_with_max_tokens_parameter(self, client):
        payload = {"query": "¿Procedimiento de报销?", "max_tokens": 500}
        with patch("app.api.endpoints.orchestrator") as mock_orch:
            mock_orch.arun = AsyncMock(
                return_value={
                    "answer": "Para报销 debe presentar los comprobantes en un plazo de 30 días.",
                    "sources": ["procedimientos.pdf"],
                    "confidence": 0.85,
                }
            )
            response = await client.post("/query", json=payload)
            assert response.status_code == 200
            mock_orch.arun.assert_called_once()
            call_kwargs = mock_orch.arun.call_args.kwargs
            assert call_kwargs.get("max_tokens") == 500

    async def test_query_with_invalid_temperature_returns_422(self, client):
        payload = {"query": "¿Política de vacaciones?", "temperature": 2.5}
        response = await client.post("/query", json=payload)
        assert response.status_code == 422

    async def test_query_with_invalid_max_tokens_returns_422(self, client):
        payload = {"query": "¿Política de vacaciones?", "max_tokens": -10}
        response = await client.post("/query", json=payload)
        assert response.status_code == 422
// === ARCHIVO: tests/test_chains.py ===
import pytest
from unittest.mock import AsyncMock, MagicMock, patch, PropertyMock
from typing import Any

from app.chains.orchestrator import RAGOrchestrator
from app.retrieval.vector_store import VectorStore
from app.retrieval.embeddings import EmbeddingsProvider
from app.models.bedrock import BedrockClient, BedrockResponse, BedrockError
from app.prompts.templates import PromptTemplate
from app.utils.exceptions import ContextRetrievalError, BedrockInvocationError


@pytest.fixture
def mock_vector_store():
    store = MagicMock(spec=VectorStore)
    store.similarity_search = AsyncMock(
        return_value=[
            {
                "page_content": "La política de vacaciones establece 15 días hábiles anuales.",
                "metadata": {"source": "normativa_2024.pdf", "page": 1},
            },
            {
                "page_content": "Los empleados pueden acumular hasta 5 días de vacaciones.",
                "metadata": {"source": "normativa_2024.pdf", "page": 2},
            },
        ]
    )
    return store


@pytest.fixture
def mock_embeddings():
    emb = MagicMock(spec=EmbeddingsProvider)
    emb.embed_query = AsyncMock(return_value=[0.1] * 1536)
    return emb


@pytest.fixture
def mock_bedrock_client():
    client = MagicMock(spec=BedrockClient)
    client.invoke_model = AsyncMock(
        return_value=BedrockResponse(
            completion="La política de vacaciones de PragmaFintech establece 15 días hábiles anuales, con posibilidad de acumular hasta 5 días para el siguiente año.",
            stop_reason="stop",
            usage={"prompt_tokens": 50, "completion_tokens": 30},
        )
    )
    return client


@pytest.fixture
def mock_prompt_template():
    template = MagicMock(spec=PromptTemplate)
    template.format = MagicMock(
        return_value="Contexto: Las políticas establecen 15 días de vacaciones. Pregunta: ¿Cuál es la política de vacaciones? Respuesta:"
    )
    return template


@pytest.fixture
def orchestrator(mock_vector_store, mock_embeddings, mock_bedrock_client, mock_prompt_template):
    return RAGOrchestrator(
        vector_store=mock_vector_store,
        embeddings=mock_embeddings,
        bedrock_client=mock_bedrock_client,
        prompt_template=mock_prompt_template,
    )


@pytest.mark.unit
class TestRAGOrchestrator:
    @pytest.mark.asyncio
    async def test_retrieval_returns_context(self, orchestrator, mock_vector_store):
        result = await orchestrator.arun(query="¿Cuál es la política de vacaciones?")
        assert "answer" in result
        assert "sources" in result
        mock_vector_store.similarity_search.assert_called_once()

    @pytest.mark.asyncio
    async def test_retrieval_empty_context_raises_error(self, mock_vector_store, mock_embeddings, mock_bedrock_client, mock_prompt_template):
        mock_vector_store.similarity_search = AsyncMock(return_value=[])
        orch = RAGOrchestrator(
            vector_store=mock_vector_store,
            embeddings=mock_embeddings,
            bedrock_client=mock_bedrock_client,
            prompt_template=mock_prompt_template,
        )
        with pytest.raises(ContextRetrievalError):
            await orch.arun(query="¿Política inexistente?")

    @pytest.mark.asyncio
    async def test_generation_uses_retrieved_context(self, orchestrator, mock_bedrock_client):
        result = await orchestrator.arun(query="¿Política de vacaciones?")
        assert result["answer"] is not None
        assert len(result["answer"]) > 0
        mock_bedrock_client.invoke_model.assert_called_once()

    @pytest.mark.asyncio
    async def test_sources_extracted_from_metadata(self, orchestrator, mock_vector_store):
        result = await orchestrator.arun(query="¿Vacaciones?")
        assert "sources" in result
        assert len(result["sources"]) > 0

    @pytest.mark.asyncio
    async def test_bedrock_error_raises_bedrock_error(self, mock_vector_store, mock_embeddings, mock_bedrock_client, mock_prompt_template):
        mock_bedrock_client.invoke_model = AsyncMock(
            side_effect=BedrockError("Model timeout")
        )
        orch = RAGOrchestrator(
            vector_store=mock_vector_store,
            embeddings=mock_embeddings,
            bedrock_client=mock_bedrock_client,
            prompt_template=mock_prompt_template,
        )
        with pytest.raises(BedrockInvocationError):
            await orch.arun(query="¿Política?")

    @pytest.mark.asyncio
    async def test_temperature_parameter_passed_to_bedrock(self, mock_vector_store, mock_embeddings, mock_bedrock_client, mock_prompt_template):
        orch = RAGOrchestrator(
            vector_store=mock_vector_store,
            embeddings=mock_embeddings,
            bedrock_client=mock_bedrock_client,
            prompt_template=mock_prompt_template,
        )
        await orch.arun(query="¿Vacaciones?", temperature=0.9)
        call_kwargs = mock_bedrock_client.invoke_model.call_args.kwargs
        assert "temperature" in str(call_kwargs) or call_kwargs.get("temperature") == 0.9

    @pytest.mark.asyncio
    async def test_max_tokens_parameter_passed_to_bedrock(self, mock_vector_store, mock_embeddings, mock_bedrock_client, mock_prompt_template):
        orch = RAGOrchestrator(
            vector_store=mock_vector_store,
            embeddings=mock_embeddings,
            bedrock_client=mock_bedrock_client,
            prompt_template=mock_prompt_template,
        )
        await orch.arun(query="¿Vacaciones?", max_tokens=300)
        call_kwargs = mock_bedrock_client.invoke_model.call_args.kwargs
        assert "max_tokens" in str(call_kwargs) or call_kwargs.get("max_tokens") == 300

    @pytest.mark.asyncio
    async def test_confidence_score_calculation(self, orchestrator):
        result = await orchestrator.arun(query="¿Vacaciones?")
        assert "confidence" in result
        assert 0.0 <= result["confidence"] <= 1.0


@pytest.mark.unit
class TestRAGOrchestratorEdgeCases:
    @pytest.mark.asyncio
    async def test_very_long_query_truncates(self, mock_vector_store, mock_embeddings, mock_bedrock_client, mock_prompt_template):
        long_query = "¿" + "Política ".repeat(1000) + "?"
        orch = RAGOrchestrator(
            vector_store=mock_vector_store,
            embeddings=mock_embeddings,
            bedrock_client=mock_bedrock_client,
            prompt_template=mock_prompt_template,
        )
        result = await orch.arun(query=long_query)
        assert "answer" in result

    @pytest.mark.asyncio
    async def test_multiple_sources_merged(self, mock_vector_store, mock_embeddings, mock_bedrock_client, mock_prompt_template):
        mock_vector_store.similarity_search = AsyncMock(
            return_value=[
                {"page_content": "Contenido del doc 1", "metadata": {"source": "doc1.pdf"}},
                {"page_content": "Contenido del doc 2", "metadata": {"source": "doc2.pdf"}},
                {"page_content": "Contenido del doc 3", "metadata": {"source": "doc1.pdf"}},
            ]
        )
        orch = RAGOrchestrator(
            vector_store=mock_vector_store,
            embeddings=mock_embeddings,
            bedrock_client=mock_bedrock_client,
            prompt_template=mock_prompt_template,
        )
        result = await orch.arun(query="¿Info?")
        unique_sources = set(result["sources"])
        assert len(unique_sources) == 2

    @pytest.mark.asyncio
    async def test_empty_answer_handled_gracefully(self, mock_vector_store, mock_embeddings, mock_bedrock_client, mock_prompt_template):
        mock_bedrock_client.invoke_model = AsyncMock(
            return_value=BedrockResponse(
                completion="",
                stop_reason="stop",
                usage={"prompt_tokens": 50, "completion_tokens": 0},
            )
        )
        orch = RAGOrchestrator(
            vector_store=mock_vector_store,
            embeddings=mock_embeddings,
            bedrock_client=mock_bedrock_client,
            prompt_template=mock_prompt_template,
        )
        result = await orch.arun(query="¿Vacaciones?")
        assert result["answer"] == ""
// === ARCHIVO: tests/test_eval.py ===
import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from typing import Any
import json

from app.eval.evaluation import EvaluationRunner, TestCase, EvaluationResult
from app.eval.metrics import (
    calculate_exact_match,
    calculate_semantic_similarity,
    calculate_retrieval_precision,
    calculate_answer_relevance,
)
from app.utils.exceptions import EvaluationError


@pytest.fixture
def sample_test_cases():
    return [
        TestCase(
            id="tc_001",
            query="¿Cuál es la política de vacaciones?",
            expected_answer="15 días hábiles anuales",
            context_docs=["normativa_2024.pdf"],
            metadata={"category": "laboral"},
        ),
        TestCase(
            id="tc_002",
            query="¿Cuántos días de permiso por enfermedad corresponden?",
            expected_answer="10 días por año",
            context_docs=["normativa_2024.pdf"],
            metadata={"category": "laboral"},
        ),
        TestCase(
            id="tc_003",
            query="¿Cuál es el procedimiento de报销?",
            expected_answer="Presentar comprobantes en 30 días",
            context_docs=["procedimientos.pdf"],
            metadata={"category": "gastos"},
        ),
    ]


@pytest.fixture
def mock_orchestrator():
    orch = MagicMock()
    orch.arun = AsyncMock(
        return_value={
            "answer": "La política establece 15 días hábiles de vacaciones anuales.",
            "sources": ["normativa_2024.pdf"],
            "confidence": 0.92,
        }
    )
    return orch


@pytest.mark.unit
class TestEvaluationRunner:
    def test_evaluation_runner_initialization(self, sample_test_cases):
        runner = EvaluationRunner(test_cases=sample_test_cases)
        assert runner.test_cases == sample_test_cases
        assert len(runner.test_cases) == 3

    @pytest.mark.asyncio
    async def test_run_evaluation_returns_results(self, sample_test_cases, mock_orchestrator):
        runner = EvaluationRunner(test_cases=sample_test_cases, orchestrator=mock_orchestrator)
        results = await runner.run_evaluation()
        assert len(results) == 3
        assert all(isinstance(r, EvaluationResult) for r in results)

    @pytest.mark.asyncio
    async def test_evaluation_collects_metrics(self, sample_test_cases, mock_orchestrator):
        runner = EvaluationRunner(test_cases=sample_test_cases, orchestrator=mock_orchestrator)
        results = await runner.run_evaluation()
        for result in results:
            assert hasattr(result, "exact_match")
            assert hasattr(result, "semantic_similarity")
            assert hasattr(result, "retrieval_precision")

    @pytest.mark.asyncio
    async def test_evaluation_error_raises_exception(self, sample_test_cases):
        broken_orch = MagicMock()
        broken_orch.arun = AsyncMock(side_effect=RuntimeError("Broken orchestrator"))
        runner = EvaluationRunner(test_cases=sample_test_cases, orchestrator=broken_orch)
        with pytest.raises(EvaluationError):
            await runner.run_evaluation()

    @pytest.mark.asyncio
    async def test_evaluation_with_empty_answers(self, sample_test_cases, mock_orchestrator):
        mock_orchestrator.arun = AsyncMock(
            return_value={"answer": "", "sources": [], "confidence": 0.0}
        )
        runner = EvaluationRunner(test_cases=sample_test_cases, orchestrator=mock_orchestrator)
        results = await runner.run_evaluation()
        assert all(r.exact_match == 0.0 for r in results)


@pytest.mark.unit
class TestMetrics:
    def test_exact_match_identical(self):
        score = calculate_exact_match("Hola mundo", "Hola mundo")
        assert score == 1.0

    def test_exact_match_different(self):
        score = calculate_exact_match("Hola mundo", "Adiós mundo")
        assert score == 0.0

    def test_exact_match_partial(self):
        score = calculate_exact_match("La política de vacaciones", "La política")
        assert 0.0 < score < 1.0

    def test_exact_match_case_insensitive(self):
        score = calculate_exact_match("Hola Mundo", "hola mundo")
        assert score == 1.0

    def test_semantic_similarity_identical(self):
        score = calculate_semantic_similarity("El perro corre rápido", "El perro corre rápido")
        assert score >= 0.95

    def test_semantic_similarity_similar(self):
        score = calculate_semantic_similarity("El gato duerme", "El felino descansa")
        assert 0.5 <= score <= 0.95

    def test_semantic_similarity_different(self):
        score = calculate_semantic_similarity("Computadora", "Zanahoria")
        assert score < 0.3

    def test_retrieval_precision_all_relevant(self):
        retrieved = ["doc1.pdf", "doc2.pdf", "doc3.pdf"]
        relevant = ["doc1.pdf", "doc2.pdf"]
        precision = calculate_retrieval_precision(retrieved, relevant)
        assert precision == 1.0

    def test_retrieval_precision_partial(self):
        retrieved = ["doc1.pdf", "doc4.pdf"]
        relevant = ["doc1.pdf", "doc2.pdf"]
        precision = calculate_retrieval_precision(retrieved, relevant)
        assert precision == 0.5

    def test_retrieval_precision_none(self):
        retrieved = ["doc4.pdf", "doc5.pdf"]
        relevant = ["doc1.pdf", "doc2.pdf"]
        precision = calculate_retrieval_precision(retrieved, relevant)
        assert precision == 0.0

    def test_retrieval_precision_empty_retrieved(self):
        precision = calculate_retrieval_precision([], ["doc1.pdf"])
        assert precision == 0.0

    def test_answer_relevance_high(self):
        relevance = calculate_answer_relevance(
            query="¿Cuál es la política de vacaciones?",
            answer="La política establece 15 días de vacaciones anuales para todos los empleados.",
        )
        assert relevance >= 0.7

    def test_answer_relevance_low(self):
        relevance = calculate_answer_relevance(
            query="¿Política de vacaciones?",
            answer="El cielo está azul hoy.",
        )
        assert relevance < 0.3

    def test_answer_relevance_empty_answer(self):
        relevance = calculate_answer_relevance(
            query="¿Política de vacaciones?",
            answer="",
        )
        assert relevance == 0.0


@pytest.mark.unit
class TestEvaluationResult:
    def test_evaluation_result_creation(self):
        result = EvaluationResult(
            test_case_id="tc_001",
            query="¿Pregunta?",
            expected_answer="Respuesta esperada",
            actual_answer="Respuesta real",
            sources=["doc1.pdf"],
            confidence=0.85,
            exact_match=0.6,
            semantic_similarity=0.8,
            retrieval_precision=1.0,
            answer_relevance=0.75,
        )
        assert result.test_case_id == "tc_001"
        assert result.confidence == 0.85

    def test_evaluation_result_to_dict(self):
        result = EvaluationResult(
            test_case_id="tc_001",
            query="¿Pregunta?",
            expected_answer="Respuesta esperada",
            actual_answer="Respuesta real",
            sources=["doc1.pdf"],
            confidence=0.85,
            exact_match=0.6,
            semantic_similarity=0.8,
            retrieval_precision=1.0,
            answer_relevance=0.75,
        )
        result_dict = result.to_dict()
        assert isinstance(result_dict, dict)
        assert result_dict["test_case_id"] == "tc_001"

    def test_evaluation_result_overall_score(self):
        result = EvaluationResult(
            test_case_id="tc_001",
            query="¿Pregunta?",
            expected_answer="Respuesta esperada",
            actual_answer="Respuesta real",
            sources=["doc1.pdf"],
            confidence=0.85,
            exact_match=0.6,
            semantic_similarity=0.8,
            retrieval_precision=1.0,
            answer_relevance=0.75,
        )
        overall = result.overall_score()
        assert 0.0 <= overall <= 1.0
        expected_score = (0.6 + 0.8 + 1.0 + 0.75) / 4
        assert overall == expected_score


terraform {
  required_version = ">= 1.7.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.50"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }

  backend "s3" {
    bucket = "pragma-normativa-terraform-state"
    key    = "infra/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project        = "pragma-normativa-rag"
      Environment    = var.environment
      ManagedBy      = "terraform"
      CostCenter     = "Engineering"
      Compliance     = "internal"
    }
  }

  skip_credentials_validation = var.is_local
  skip_requesting_account_id  = var.is_local
  skip_metadata_api_check     = var.is_local
}

resource "random_id" "suffix" {
  byte_length = 8
}

resource "aws_s3_bucket" "artifacts" {
  bucket = "pragma-normativa-artifacts-${random_id.suffix.hex}"

  tags = {
    Name        = "pragma-normativa-artifacts"
    Environment = var.environment
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "artifacts" {
  bucket = aws_s3_bucket.artifacts.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_iam_role" "lambda_execution" {
  name = "pragma-normativa-lambda-role-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Environment = var.environment
  }
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_policy" "lambda_secrets" {
  name = "pragma-normativa-lambda-secrets-${var.environment}"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue",
          "secretsmanager:DescribeSecret"
        ]
        Resource = var.secrets_manager_arns
      },
      {
        Effect = "Allow"
        Action = [
          "ssm:GetParameter",
          "ssm:GetParameters",
          "ssm:GetParametersByPath"
        ]
        Resource = "arn:aws:ssm:${var.aws_region}:${var.account_id}:parameter/pragma-normativa/*"
      }
    ]
  })

  tags = {
    Environment = var.environment
  }
}

resource "aws_iam_policy" "lambda_bedrock" {
  name = "pragma-normativa-lambda-bedrock-${var.environment}"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "bedrock:InvokeModel",
          "bedrock:InvokeModelWithResponseStream",
          "bedrock:ListFoundationModels",
          "bedrock:GetFoundationModel"
        ]
        Resource = "arn:aws:bedrock:${var.aws_region}::foundation-model/${var.bedrock_model_id}"
      }
    ]
  })

  tags = {
    Environment = var.environment
  }
}

resource "aws_iam_policy" "lambda_opensearch" {
  name = "pragma-normativa-lambda-opensearch-${var.environment}"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "es:ESHttp*"
        ]
        Resource = aws_opensearch_domain.main.arn
      }
    ]
  })

  tags = {
    Environment = var.environment
  }
}

resource "aws_iam_role_policy_attachment" "lambda_secrets" {
  role       = aws_iam_role.lambda_execution.name
  policy_arn = aws_iam_policy.lambda_secrets.arn
}

resource "aws_iam_role_policy_attachment" "lambda_bedrock" {
  role       = aws_iam_role.lambda_execution.name
  policy_arn = aws_iam_policy.lambda_bedrock.arn
}

resource "aws_iam_role_policy_attachment" "lambda_opensearch" {
  role       = aws_iam_role.lambda_execution.name
  policy_arn = aws_iam_policy.lambda_opensearch.arn
}

resource "aws_iam_role_policy_attachment" "lambda_vpc" {
  count      = var.enable_vpc ? 1 : 0
  role       = aws_iam_role.lambda_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

resource "aws_iam_policy" "lambda_logging" {
  name = "pragma-normativa-lambda-logging-${var.environment}"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:${var.aws_region}:${var.account_id}:log-group:/aws/lambda/pragma-normativa*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_logging" {
  role       = aws_iam_role.lambda_execution.name
  policy_arn = aws_iam_policy.lambda_logging.arn
}

resource "aws_lambda_function" "api" {
  filename         = data.archive_file.lambda.output_path
  function_name    = "pragma-normativa-api-${var.environment}"
  role            = aws_iam_role.lambda_execution.arn
  handler         = "app.main:create_app"
  source_code_hash = data.archive_file.lambda.output_base64sha256
  runtime         = "python3.13"
  timeout         = var.lambda_timeout
  memory_size     = var.lambda_memory_size
  ephemeral_storage {
    size = var.lambda_ephemeral_storage
  }

  environment {
    variables = {
      ENVIRONMENT          = var.environment
      AWS_REGION           = var.aws_region
      LOG_LEVEL            = var.log_level
      BEDROCK_MODEL_ID     = var.bedrock_model_id
      BEDROCK_MODEL_KWARGS = var.bedrock_model_kwargs
      OPENSEARCH_ENDPOINT  = aws_opensearch_domain.main.endpoint
      OPENSEARCH_INDEX     = var.opensearch_index
      EMBEDDING_MODEL      = var.embedding_model
      TEMPERATURE          = var.temperature
      MAX_TOKENS           = var.max_tokens
      CORS_ORIGINS         = var.cors_origins
      ENABLE_EVALUATION    = var.enable_evaluation
      METRICS_NAMESPACE    = "Pragma/NormativaRAG"
      METRICS_ENABLED      = var.enable_metrics
    }
  }

  dynamic "vpc_config" {
    for_each = var.enable_vpc ? [1] : []
    content {
      subnet_ids         = var.vpc_subnet_ids
      security_group_ids = var.vpc_security_group_ids
    }
  }

  depends_on = [
    aws_iam_role_policy_attachment.lambda_basic_execution,
    aws_iam_role_policy_attachment.lambda_logging
  ]

  tags = {
    Environment = var.environment
    Function    = "api"
  }
}

resource "aws_lambda_function_url" "api" {
  function_name      = aws_lambda_function.api.function_name
  authorization_type = "AWS_IAM"
  cors {
    allow_credentials    = true
    allow_origins        = var.cors_origins_list
    allow_methods        = ["GET", "POST", "OPTIONS"]
    allow_headers        = ["Authorization", "Content-Type", "X-Request-ID"]
    expose_headers       = ["X-Request-ID", "X-Response-Time"]
    max_age              = 3600
  }
}

resource "aws_lambda_permission" "api_gateway" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.api.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.main.execution_arn}/*/*"
}

resource "aws_api_gateway_rest_api" "main" {
  name        = "pragma-normativa-api-${var.environment}"
  description = "API de consulta normativa con modelos generativos"

  endpoint_configuration {
    types = [var.api_gateway_type]
  }

  tags = {
    Environment = var.environment
  }
}

resource "aws_api_gateway_resource" "proxy" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_rest_api.main.root_resource_id
  path_part   = "{proxy+}"
}

resource "aws_api_gateway_method" "any" {
  rest_api_id   = aws_api_gateway_rest_api.main.id
  resource_id   = aws_api_gateway_resource.proxy.id
  http_method   = "ANY"
  authorization = "AWS_IAM"

  request_parameters = {
    "method.request.path.proxy" = true
  }
}

resource "aws_api_gateway_integration" "lambda" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  resource_id = aws_api_gateway_resource.proxy.id
  http_method = aws_api_gateway_method.any.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.api.invoke_arn

  cache_namespace = "pragma-normativa"

  request_parameters = {
    "integration.request.path.proxy" = "method.request.path.proxy"
  }
}

resource "aws_api_gateway_resource" "root" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_rest_api.main.root_resource_id
  path_part   = "query"
}

resource "aws_api_gateway_method" "query_post" {
  rest_api_id   = aws_api_gateway_rest_api.main.id
  resource_id   = aws_api_gateway_resource.root.id
  http_method   = "POST"
  authorization = "AWS_IAM"
}

resource "aws_api_gateway_integration" "query_lambda" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  resource_id = aws_api_gateway_resource.root.id
  http_method = aws_api_gateway_method.query_post.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.api.invoke_arn
}

resource "aws_api_gateway_resource" "health" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_rest_api.main.root_resource_id
  path_part   = "health"
}

resource "aws_api_gateway_method" "health_get" {
  rest_api_id   = aws_api_gateway_rest_api.main.id
  resource_id   = aws_api_gateway_resource.health.id
  http_method   = "GET"
  authorization = "AWS_IAM"
}

resource "aws_api_gateway_integration" "health_lambda" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  resource_id = aws_api_gateway_resource.health.id
  http_method = aws_api_gateway_method.health_get.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.api.invoke_arn
}

resource "aws_api_gateway_deployment" "main" {
  rest_api_id = aws_api_gateway_rest_api.main.id

  depends_on = [
    aws_api_gateway_integration.lambda,
    aws_api_gateway_integration.query_lambda,
    aws_api_gateway_integration.health_lambda
  ]

  lifecycle {
    create_before_destroy = true
  }

  variables = {
    deployed_at = timestamp()
  }
}

resource "aws_api_gateway_stage" "prod" {
  deployment_id = aws_api_gateway_deployment.main.id
  rest_api_id   = aws_api_gateway_rest_api.main.id
  stage_name    = var.environment

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gateway.arn
    format         = "$context.requestId: $context.endpoint $context.httpMethod $context.status $context.responseLatency $context.requestTime"
  }

  tags = {
    Environment = var.environment
  }
}

resource "aws_api_gateway_usage_plan" "main" {
  name = "pragma-normativa-usage-plan-${var.environment}"

  api_stages {
    api_id = aws_api_gateway_rest_api.main.id
    stage  = aws_api_gateway_stage.prod.stage_name
  }

  quota_settings {
    limit  = var.api_usage_quota_limit
    period = "MONTH"
  }

  throttle_settings {
    burst_limit = var.api_throttle_burst_limit
    rate_limit  = var.api_throttle_rate_limit
  }

  tags = {
    Environment = var.environment
  }
}

resource "aws_api_gateway_api_key" "main" {
  name = "pragma-normativa-api-key-${var.environment}"

  tags = {
    Environment = var.environment
  }
}

resource "aws_api_gateway_usage_plan_key" "main" {
  key_id        = aws_api_gateway_api_key.main.id
  key_type      = "API_KEY"
  usage_plan_id = aws_api_gateway_usage_plan.main.id
}

resource "aws_cloudwatch_log_group" "lambda" {
  name              = "/aws/lambda/pragma-normativa-api-${var.environment}"
  retention_in_days = var.log_retention_days

  tags = {
    Environment = var.environment
  }
}

resource "aws_cloudwatch_log_group" "api_gateway" {
  name              = "/aws/apigateway/pragma-normativa-api-${var.environment}"
  retention_in_days = var.log_retention_days

  tags = {
    Environment = var.environment
  }
}

resource "aws_opensearch_domain" "main" {
  domain_name    = "pragma-normativa-${var.environment}"
  engine_version = var.opensearch_version

  cluster_config {
    instance_type            = var.opensearch_instance_type
    instance_count           = var.opensearch_instance_count
    dedicated_master_enabled = var.opensearch_dedicated_master
    dedicated_master_type    = var.opensearch_master_type
    dedicated_master_count   = var.opensearch_master_count
    zone_awareness_enabled   = var.opensearch_zone_awareness
  }

  ebs_options {
    ebs_enabled = true
    volume_type = var.opensearch_volume_type
    volume_size = var.opensearch_volume_size
  }

  access_policies = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          AWS = aws_iam_role.lambda_execution.arn
        }
        Action = [
          "es:ESHttpGet",
          "es:ESHttpPut",
          "es:ESHttpPost",
          "es:ESHttpDelete",
          "es:ESHttpHead"
        ]
        Resource = "${aws_opensearch_domain.main.arn}/*"
      }
    ]
  })

  log_publishing_options {
    cloudwatch_log_group_arn = aws_cloudwatch_log_group.opensearch.arn
    enabled                  = true
    log_type                 = "SEARCH_SLOW_LOGS"
  }

  domain_endpoint_options {
    enforce.https       = true
    tls                 = "1.2"
    custom_endpoint_enabled = var.enable_custom_endpoint
    custom_endpoint         = var.custom_endpoint_domain
  }

  tags = {
    Environment = var.environment
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_cloudwatch_log_group" "opensearch" {
  name              = "/aws/opensearch/pragma-normativa-${var.environment}"
  retention_in_days = var.log_retention_days

  tags = {
    Environment = var.environment
  }
}

resource "aws_lambda_event_invoke_config" "api" {
  function_name = aws_lambda_function.api.function_name
  qualifier     = aws_lambda_function.api.version

  destination_config {
    on_failure {
      destination = aws_sns_topic.lambda_failures.arn
    }
    on_success {
      destination = aws_sns_topic.lambda_success.arn
    }
  }

  maximum_event_age_in_seconds = 3600
  maximum_retry_attempts       = 2
}

resource "aws_sns_topic" "lambda_failures" {
  name = "pragma-normativa-lambda-failures-${var.environment}"

  tags = {
    Environment = var.environment
  }
}

resource "aws_sns_topic" "lambda_success" {
  name = "pragma-normativa-lambda-success-${var.environment}"

  tags = {
    Environment = var.environment
  }
}

resource "aws_sns_topic_policy" "lambda_failures" {
  arn    = aws_sns_topic.lambda_failures.arn
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action = "sns:Publish"
        Resource = aws_sns_topic.lambda_failures.arn
      }
    ]
  })
}

resource "aws_cloudwatch_metric_alarm" "lambda_errors" {
  alarm_name          = "pragma-normativa-lambda-errors-${var.environment}"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = "300"
  statistic           = "Sum"
  threshold           = "0"
  alarm_description   = "This metric monitors lambda function errors"

  dimensions = {
    FunctionName = aws_lambda_function.api.function_name
  }

  alarm_actions = [aws_sns_topic.lambda_failures.arn]
  ok_actions    = [aws_sns_topic.lambda_success.arn]

  tags = {
    Environment = var.environment
  }
}

resource "aws_cloudwatch_metric_alarm" "lambda_throttles" {
  alarm_name          = "pragma-normativa-lambda-throttles-${var.environment}"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "Throttles"
  namespace           = "AWS/Lambda"
  period              = "300"
  statistic           = "Sum"
  threshold           = "0"
  alarm_description   = "This metric monitors lambda function throttles"

  dimensions = {
    FunctionName = aws_lambda_function.api.function_name
  }

  alarm_actions = [aws_sns_topic.lambda_failures.arn]

  tags = {
    Environment = var.environment
  }
}

resource "aws_cloudwatch_metric_alarm" "lambda_duration" {
  alarm_name          = "pragma-normativa-lambda-duration-${var.environment}"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "Duration"
  namespace           = "AWS/Lambda"
  period              = "300"
  statistic           = "Maximum"
  threshold           = var.lambda_duration_threshold
  alarm_description   = "This metric monitors lambda function duration"

  dimensions = {
    FunctionName = aws_lambda_function.api.function_name
  }

  alarm_actions = [aws_sns_topic.lambda_failures.arn]

  tags = {
    Environment = var.environment
  }
}

resource "aws_cloudwatch_metric_alarm" "opensearch_cluster_status" {
  alarm_name          = "pragma-normativa-opensearch-cluster-${var.environment}"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "ClusterStatus.green"
  namespace           = "AWS/OpenSearchService"
  period              = "60"
  statistic           = "Maximum"
  threshold           = "1"
  alarm_description   = "This metric monitors OpenSearch cluster health"

  dimensions = {
    DomainName = aws_opensearch_domain.main.domain_name
    ClientId   = var.account_id
  }

  alarm_actions = [aws_sns_topic.lambda_failures.arn]

  tags = {
    Environment = var.environment
  }
}

data "archive_file" "lambda" {
  type        = "zip"
  source_dir  = var.lambda_source_dir
  output_path = "/tmp/lambda_function.zip"

  excludes = [
    ".pytest_cache",
    "__pycache__",
    "*.pyc",
    ".venv",
    "venv",
    ".git",
  ]
}

resource "null_resource" "validate_dependencies" {
  triggers = {
    python_version = var.python_version
    dependencies   = filemd5(var.lambda_requirements_file)
  }

  provisioner "local-exec" {
    command = "pip install -r ${var.lambda_requirements_file} -t /tmp/lambda_deps && echo 'Dependencies validated'"
  }
}

resource "aws_s3_object" "lambda_package" {
  bucket = aws_s3_bucket.artifacts.id
  key    = "lambda/pragma-normativa-${var.environment}.zip"
  source = data.archive_file.lambda.output_path

  etag = filemd5(data.archive_file.lambda.output_path)

  tags = {
    Environment = var.environment
  }
}

resource "aws_kms_key" "secrets" {
  description             = "KMS key for pragma-normativa secrets"
  deletion_window_in_days = 10
  enable_key_rotation     = true

  policy = jsonencode({
    Version = "2012-10-17"
    Id      = "key-policy"
    Statement = [
      {
        Sid = "Enable IAM User Permissions"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${var.account_id}:root"
        }
        Action = "kms:*"
        Resource = "*"
      },
      {
        Sid = "Allow Lambda to use key"
        Effect = "Allow"
        Principal = {
          AWS = aws_iam_role.lambda_execution.arn
        }
        Action = [
          "kms:Decrypt",
          "kms:Encrypt",
          "kms:GenerateDataKey"
        ]
        Resource = "*"
      }
    ]
  })

  tags = {
    Environment = var.environment
  }
}

resource "aws_kms_alias" "secrets" {
  name          = "alias/pragma-normativa-${var.environment}"
  target_key_id = aws_kms_key.secrets.key_id
}

resource "aws_dynamodb_table" "audit_logs" {
  name           = "pragma-normativa-audit-${var.environment}"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "pk"
  range_key      = "sk"

  attribute {
    name = "pk"
    type = "S"
  }

  attribute {
    name = "sk"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "S"
  }

  attribute {
    name = "user_id"
    type = "S"
  }

  global_secondary_index {
    name            = "timestamp-index"
    hash_key        = "pk"
    range_key       = "timestamp"
    projection_type = "ALL"
  }

  global_secondary_index {
    name            = "user-id-index"
    hash_key        = "user_id"
    range_key       = "timestamp"
    projection_type = "ALL"
  }

  server_side_encryption {
    enabled     = true
    kms_key_arn = aws_kms_key.secrets.arn
  }

  ttl {
    attribute_name = "ttl"
    enabled        = true
  }

  tags = {
    Environment = var.environment
  }
}

resource "aws_iam_policy" "dynamodb_audit" {
  name = "pragma-normativa-dynamodb-audit-${var.environment}"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:PutItem",
          "dynamodb:GetItem",
          "dynamodb:Query",
          "dynamodb:Scan"
        ]
        Resource = aws_dynamodb_table.audit_logs.arn
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_dynamodb_audit" {
  role       = aws_iam_role.lambda_execution.name
  policy_arn = aws_iam_policy.dynamodb_audit.arn
}

resource "aws_wafv2_web_acl" "api_gateway" {
  name        = "pragma-normativa-waf-${var.environment}"
  description = "WAF for Pragma Normativa API"
  scope       = "REGIONAL"

  default_action {
    allow {}
  }

  rule {
    name     = "AWSManagedRulesCommonRuleSet"
    priority = 1

    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesCommonRuleSet"
        vendor_name = "AWS"
      }
    }

    action {
      count {}
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      sampled_requests_enabled   = true
      metric_name                = "AWSManagedRulesCommonRuleSet"
    }
  }

  rule {
    name     = "RateLimitRule"
    priority = 2

    statement {
      rate_based_statement {
        limit              = var.waf_rate_limit
        evaluation_window_duration = 60
        aggregate_key_type = "IP"
      }
    }

    action {
      block {}
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      sampled_requests_enabled   = true
      metric_name                = "RateLimitRule"
    }
  }

  visibility_config {
    cloudwatch_metrics_enabled = true
    sampled_requests_enabled   = true
    metric_name                = "pragma-normativa-waf"
  }

  tags = {
    Environment = var.environment
  }
}

resource "aws_wafv2_web_acl_association" "api_gateway" {
  resource_arn = aws_api_gateway_stage.prod.arn
  web_acl_arn  = aws_wafv2_web_acl.api_gateway.arn
}

// === ARCHIVO: infra/terraform/outputs.tf ===
output "api_gateway_url" {
  description = "URL base del API Gateway para consultas normativas"
  value       = "${aws_api_gateway_stage.prod.invoke_url}"
}

output "api_gateway_arn" {
  description = "ARN del API Gateway"
  value       = aws_api_gateway_rest_api.main.arn
}

output "api_gateway_execution_arn" {
  description = "ARN de ejecución del API Gateway"
  value       = aws_api_gateway_rest_api.main.execution_arn
}

output "lambda_function_name" {
  description = "Nombre de la función Lambda que sirve la API"
  value       = aws_lambda_function.api.function_name
}

output "lambda_function_arn" {
  description = "ARN de la función Lambda"
  value       = aws_lambda_function.api.arn
}

output "lambda_function_version" {
  description = "Versión actual de la función Lambda"
  value       = aws_lambda_function.api.version
}

output "lambda_iam_role_arn" {
  description = "ARN del rol de ejecución de Lambda"
  value       = aws_iam_role.lambda_execution.arn
}

output "lambda_function_url" {
  description = "URL directa de la función Lambda (sin API Gateway)"
  value       = aws_lambda_function_url.api.function_url
}

output "opensearch_domain_endpoint" {
  description = "Endpoint del dominio OpenSearch para búsqueda vectorial"
  value       = aws_opensearch_domain.main.endpoint
}

output "opensearch_domain_arn" {
  description = "ARN del dominio OpenSearch"
  value       = aws_opensearch_domain.main.arn
}

output "opensearch_domain_id" {
  description = "ID del dominio OpenSearch"
  value       = aws_opensearch_domain.main.domain_id
}

output "opensearch_security_group_id" {
  description = "ID del security group de OpenSearch"
  value       = var.enable_vpc ? aws_opensearch_domain.main.vpc_options[0].security_group_ids[0] : ""
}

output "s3_artifacts_bucket" {
  description = "Bucket S3 para artefactos del pipeline"
  value       = aws_s3_bucket.artifacts.id
}

output "dynamodb_audit_table" {
  description = "Tabla DynamoDB para logs de auditoría"
  value       = aws_dynamodb_table.audit_logs.name
}

output "dynamodb_audit_table_arn" {
  description = "ARN de la tabla DynamoDB de auditoría"
  value       = aws_dynamodb_table.audit_logs.arn
}

output "kms_key_arn" {
  description = "ARN de la clave KMS para secretos"
  value       = aws_kms_key.secrets.arn
}

output "waf_web_acl_arn" {
  description = "ARN del Web ACL de WAF"
  value       = aws_wafv2_web_acl.api_gateway.arn
}

output "cloudwatch_log_group_lambda" {
  description = "Nombre del grupo de logs de CloudWatch para Lambda"
  value       = aws_cloudwatch_log_group.lambda.name
}

output "cloudwatch_log_group_api_gateway" {
  description = "Nombre del grupo de logs de CloudWatch para API Gateway"
  value       = aws_cloudwatch_log_group.api_gateway.name
}

output "sns_topic_lambda_failures" {
  description = "ARN del topic SNS para notificaciones de fallos en Lambda"
  value       = aws_sns_topic.lambda_failures.arn
}

output "sns_topic_lambda_success" {
  description = "ARN del topic SNS para notificaciones de éxito en Lambda"
  value       = aws_sns_topic.lambda_success.arn
}

output "api_usage_plan_id" {
  description = "ID del usage plan del API Gateway"
  value       = aws_api_gateway_usage_plan.main.id
}

output "api_key_id" {
  description = "ID de la API Key configurada"
  value       = aws_api_gateway_api_key.main.id
}

output "api_key_value" {
  description = "Valor de la API Key (solo disponible en creación)"
  value       = aws_api_gateway_api_key.main.value
  sensitive   = true
}

output "environment" {
  description = "Ambiente de despliegue"
  value       = var.environment
}

output "aws_region" {
  description = "Región de AWS"
  value       = var.aws_region
}

output "account_id" {
  description = "ID de la cuenta de AWS"
  value       = var.account_id
}

output "deployment_timestamp" {
  description = "Timestamp del despliegue"
  value       = aws_api_gateway_deployment.main.variables.deployed_at
}

output "bedrock_model_id" {
  description = "ID del modelo de Bedrock configurado"
  value       = var.bedrock_model_id
}

output "opensearch_index" {
  description = "Nombre del índice de OpenSearch"
  value       = var.opensearch_index
}

output "embedding_model" {
  description = "Modelo de embeddings configurado"
  value       = var.embedding_model
}

output "vpc_id" {
  description = "ID de la VPC (si está habilitada)"
  value       = var.enable_vpc ? var.vpc_id : ""
}

output "all_resources" {
  description = "Mapa con todos los recursos creados para referencia"
  value = {
    api_gateway_id           = aws_api_gateway_rest_api.main.id
    lambda_function_name     = aws_lambda_function.api.function_name
    opensearch_domain_name   = aws_opensearch_domain.main.domain_name
    s3_artifacts_bucket      = aws_s3_bucket.artifacts.id
    dynamodb_audit_table     = aws_dynamodb_table.audit_logs.name
    kms_key_id               = aws_kms_key.secrets.key_id
    waf_web_acl_id           = aws_wafv2_web_acl.api_gateway.id
    cloudwatch_log_groups = {
      lambda        = aws_cloudwatch_log_group.lambda.name
      api_gateway   = aws_cloudwatch_log_group.api_gateway.name
      opensearch    = aws_cloudwatch_log_group.opensearch.name
    }
  }
}

output "endpoints" {
  description = "Endpoints disponibles para consumo"
  value = {
    health_check  = "${aws_api_gateway_stage.prod.invoke_url}health"
    query         = "${aws_api_gateway_stage.prod.invoke_url}query"
    query_proxy   = "${aws_api_gateway_stage.prod.invoke_url}{proxy+}"
    lambda_direct = aws_lambda_function_url.api.function_url
  }
}

output "monitoring_urls" {
  description = "URLs de monitoreo y observabilidad"
  value = {
    cloudwatch_logs_lambda        = "https://console.aws.amazon.com/cloudwatch/home?region=${var.aws_region}#logsV2:log-groups/log-group/${replace(aws_cloudwatch_log_group.lambda.name, "/", "$252F")}"
    cloudwatch_logs_apigateway    = "https://console.aws.amazon.com/cloudwatch/home?region=${var.aws_region}#logsV2:log-groups/log-group/${replace(aws_cloudwatch_log_group.api_gateway.name, "/", "$252F")}"
    cloudwatch_metrics_lambda     = "https://console.aws.amazon.com/cloudwatch/home?region=${var.aws_region}#metricsV2:graph=~();metric=AWS$252FLambda$252FErrors;namespace=AWS$252FLambda;dimensions=FunctionName${aws_lambda_function.api.function_name}"
    opensearch_dashboard          = "${aws_opensearch_domain.main.endpoint}_plugin/opensearchDashboards"
    api_gateway_stage             = "${aws_api_gateway_stage.prod.invoke_url}"
  }
}

output "costs_estimate" {
  description = "Estimación de costos mensuales de los recursos"
  value = {
    lambda_invocation_cost  = "~$${var.lambda_invocations_per_month * 0.0000002 * var.lambda_duration_average / 1000} USD"
    lambda_duration_cost    = "~$${var.lambda_invocations_per_month * var.lambda_duration_average * 0.0000166667 * var.lambda_memory_size / 1024} USD"
    api_gateway_cost        = "~$${var.api_requests_per_month * 0.0000035 + var.api_requests_per_month * 0.00000001} USD"
    opensearch_cost          = "~$${var.opensearch_instance_count * var.opensearch_instance_hourly_cost * 730} USD"
    dynamodb_cost            = "~$${var.dynamodb_write_capacity * 0.00013 + var.dynamodb_read_capacity * 0.000025} USD"
    data_transfer_estimate   = "~$${var.estimated_monthly_gb_transfer * 0.09} USD"
  }
}

```
