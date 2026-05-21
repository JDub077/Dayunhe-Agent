from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.character import Character
from app.schemas.character import CharacterOut, CharacterDetail
from app.schemas.common import ResponseWrapper

router = APIRouter(prefix="/characters", tags=["characters"])


@router.get("", response_model=ResponseWrapper[List[CharacterOut]])
def list_characters(db: Session = Depends(get_db)):
    characters = db.query(Character).filter(Character.status == "active").all()
    return ResponseWrapper(data=[
        CharacterOut.model_validate(c) for c in characters
    ])


@router.get("/{character_id}", response_model=ResponseWrapper[CharacterDetail])
def get_character(character_id: str, db: Session = Depends(get_db)):
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="角色不存在")

    data = CharacterDetail.model_validate(character)
    data.background = character.system_prompt[:200] + "..." if len(character.system_prompt) > 200 else character.system_prompt
    data.secrets_level = len(character.secrets or [])
    data.unlock_conditions = ["对话轮数>5", "好感度>10"]
    return ResponseWrapper(data=data)
