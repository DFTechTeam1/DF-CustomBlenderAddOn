from typing import Optional
from pydantic import BaseModel


class ServerStatus(BaseModel):
    status: Optional[str] = None


class ResponseLLM(BaseModel):
    data: Optional[dict] = None


class ResponseDefault(BaseModel):
    status: bool = True
    message: Optional[str] = None
    data: Optional[dict] = None
