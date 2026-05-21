from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class SessionCreate(BaseModel):
    character_id: str
    user_id: Optional[str] = "anonymous"


class SessionOut(BaseModel):
    session_id: str
    character_id: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
