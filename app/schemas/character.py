from typing import List, Optional
from pydantic import BaseModel


class CharacterBase(BaseModel):
    id: str
    name: str
    title: Optional[str] = None
    era: Optional[str] = None
    avatar_url: Optional[str] = None
    tagline: Optional[str] = None
    tags: Optional[List[str]] = None


class CharacterOut(CharacterBase):
    knowledge_nodes: Optional[List[str]] = None

    class Config:
        from_attributes = True


class CharacterDetail(CharacterOut):
    background: Optional[str] = None
    secrets_level: int = 0
    unlock_conditions: Optional[List[str]] = None
