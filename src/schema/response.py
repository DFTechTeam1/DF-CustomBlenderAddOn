from typing import Optional, Any
from pydantic import BaseModel


class ServerStatus(BaseModel):
    status: Optional[str] = None


class ResponseCluster3DModel(BaseModel):
    data: Optional[dict] = None


class ResponsePythonCodeGenerator(BaseModel):
    data: str = None


class ResponseDefault(BaseModel):
    status: bool = True
    message: Optional[str] = None
    data: Any = None
