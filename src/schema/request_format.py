from pydantic import BaseModel, field_validator, Field
from src.schema.validator import UserInputValidatorMixin


class Temperature(BaseModel):
    temperature: float = Field(default=0.1, ge=0.1, le=1.0)


class AutoClusterRequest(Temperature):
    object_name: list = None

    @field_validator("object_name")
    @classmethod
    def validate_model(cls, model: list) -> list:
        return UserInputValidatorMixin.validate_request(user_input=model)


class UserPrompt(Temperature):
    prompt: str = None

    @field_validator("prompt")
    @classmethod
    def validate_prompt(cls, prompt: str) -> str:
        return UserInputValidatorMixin.validate_request(user_input=prompt)
