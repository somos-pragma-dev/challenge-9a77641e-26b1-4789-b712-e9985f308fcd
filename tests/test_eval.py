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