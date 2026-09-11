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