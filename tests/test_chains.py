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