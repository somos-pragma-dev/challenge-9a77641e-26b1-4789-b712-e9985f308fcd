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