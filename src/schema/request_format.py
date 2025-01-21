from typing import Optional
from pydantic import BaseModel


class ModelData(BaseModel):
    model: Optional[list] = None
