from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar("T")

class ResponseWrapper(BaseModel, Generic[T]):
    code: int = 0
    message: str = "success"
    data: Optional[T] = None