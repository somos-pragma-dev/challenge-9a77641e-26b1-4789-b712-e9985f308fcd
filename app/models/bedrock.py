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