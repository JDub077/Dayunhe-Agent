from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class ChatRequest(BaseModel):
    session_id: str
    message: str
    client_timestamp: Optional[int] = None


class ChatMessageOut(BaseModel):
    message_id: str
    role: str
    content: str
    character_id: Optional[str] = None
    emotion_tag: Optional[str] = None
    plot_hook_triggered: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ChatHistoryOut(BaseModel):
    messages: List[ChatMessageOut]
    total: int
