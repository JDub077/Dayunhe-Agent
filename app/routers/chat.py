import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.message import Message
from app.models.session import Session as SessionModel
from app.models.character import Character
from app.schemas.chat import ChatRequest, ChatMessageOut, ChatHistoryOut
from app.schemas.common import ResponseWrapper
from app.services.llm_client import chat_completion

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ResponseWrapper[ChatMessageOut])
async def send_message(payload: ChatRequest, db: Session = Depends(get_db)):
    # 1. 校验 session
    session = db.query(SessionModel).filter(SessionModel.id == payload.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")

    # 2. 获取角色
    character = db.query(Character).filter(Character.id == session.character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="角色不存在")

    # 3. 保存用户消息
    user_msg = Message(
        id=uuid.uuid4(),
        session_id=session.id,
        role="user",
        content=payload.message,
    )
    db.add(user_msg)
    db.commit()

    # 4. 读取历史（最近 10 轮，不含本次）
    history = (
        db.query(Message)
        .filter(Message.session_id == session.id)
        .order_by(Message.created_at.desc())
        .offset(1)  # 跳过刚插入的用户消息
        .limit(20)
        .all()
    )
    history = list(reversed(history))

    # 5. 组装 messages
    messages = [{"role": "system", "content": character.system_prompt}]

    # 加入 few_shots（最多 3 组）
    for shot in (character.few_shots or [])[:3]:
        messages.append({"role": "user", "content": shot.get("user", "")})
        messages.append({"role": "assistant", "content": shot.get("assistant", "")})

    for msg in history:
        messages.append({"role": msg.role, "content": msg.content})

    messages.append({"role": "user", "content": payload.message})

    # 6. 调用 LLM
    assistant_content = await chat_completion(messages)

    # 7. 保存 assistant 消息
    assistant_msg = Message(
        id=uuid.uuid4(),
        session_id=session.id,
        role="assistant",
        content=assistant_content,
        emotion_tag="calm",  # TODO: 后续接入情感识别
    )
    db.add(assistant_msg)
    db.commit()
    db.refresh(assistant_msg)

    return ResponseWrapper(data=ChatMessageOut(
        message_id=str(assistant_msg.id),
        role="assistant",
        content=assistant_msg.content,
        character_id=character.id,
        emotion_tag=assistant_msg.emotion_tag,
        plot_hook_triggered=None,
        created_at=assistant_msg.created_at,
    ))


@router.get("/history", response_model=ResponseWrapper[ChatHistoryOut])
def get_history(
    session_id: str = Query(...),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")

    total = db.query(Message).filter(Message.session_id == session.id).count()
    messages = (
        db.query(Message)
        .filter(Message.session_id == session.id)
        .order_by(Message.created_at.asc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return ResponseWrapper(data=ChatHistoryOut(
        messages=[ChatMessageOut.model_validate(m) for m in messages],
        total=total,
    ))
