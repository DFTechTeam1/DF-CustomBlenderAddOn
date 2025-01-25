from pydantic import BaseModel, field_validator
from src.schema.validator import UserInputValidatorMixin


class Temperature(BaseModel):
    temperature: float = 0.3


class ModelData(Temperature):
    model: list = None

    @field_validator("model")
    @classmethod
    def validate_model(cls, model: list) -> list:
        return UserInputValidatorMixin.validate_request(user_input=model)


class UserPrompt(Temperature):
    prompt: str = None

    @field_validator("prompt")
    @classmethod
    def validate_prompt(cls, prompt: str) -> str:
        return UserInputValidatorMixin.validate_request(user_input=prompt)
