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