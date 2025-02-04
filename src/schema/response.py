from typing import Optional, Any
from pydantic import BaseModel, field_validator
from src.schema.validator import LLMVResponseValidatorMixin


class ServerStatus(BaseModel):
    status: Optional[str] = None


class ResponseCluster3DModel(BaseModel):
    data: Optional[dict] = None

    @field_validator("data")
    @classmethod
    def validate_llm_response(cls, data: dict) -> dict:
        return LLMVResponseValidatorMixin.validate_response(
            response=data, task_type="cluster"
        )


class ResponsePythonCodeGenerator(BaseModel):
    data: Optional[str] = None

    @field_validator("data")
    @classmethod
    def validate_llm_response(cls, data: str) -> str:
        return LLMVResponseValidatorMixin.validate_response(
            response=data, task_type="code"
        )


class ResponseDefault(BaseModel):
    status: bool = True
    message: Optional[str] = None
    data: Any = None
