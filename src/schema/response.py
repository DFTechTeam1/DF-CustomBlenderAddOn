from typing import Optional
from pydantic import BaseModel


class ServerStatus(BaseModel):
    status: Optional[str] = None
