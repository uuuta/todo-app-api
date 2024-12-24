from pydantic import BaseModel
from typing import Sequence

class ErrorResponse(BaseModel):
    message: str
    detail: Sequence
