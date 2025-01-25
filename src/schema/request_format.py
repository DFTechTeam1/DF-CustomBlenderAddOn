from typing import Optional
from pydantic import BaseModel


class Temperature(BaseModel):
    temperature: float = 0.3


class ModelData(Temperature):
    model: Optional[list] = None


class UserPrompt(Temperature):
    prompt: str = None
