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