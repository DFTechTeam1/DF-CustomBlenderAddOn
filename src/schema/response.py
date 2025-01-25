from typing import Optional, Any, Dict, List
from pydantic import BaseModel, field_validator
from src.schema.validator import LLMVResponseValidatorMixin


class ServerStatus(BaseModel):
    status: Optional[str] = None


class ResponseCluster3DModel(BaseModel):
    data: Optional[Dict[str, List[str]]] = None

    @field_validator("data")
    @classmethod
    def validate_pin(cls, data: dict) -> dict:
        return LLMVResponseValidatorMixin.validate_response(response=data)


class ResponsePythonCodeGenerator(BaseModel):
    data: Optional[str] = None

    @field_validator("data")
    @classmethod
    def validate_pin(cls, data: str) -> str:
        return LLMVResponseValidatorMixin.validate_response(response=data)


class ResponseDefault(BaseModel):
    status: bool = True
    message: Optional[str] = None
    data: Any = None
