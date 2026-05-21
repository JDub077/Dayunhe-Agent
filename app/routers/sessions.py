import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.session import Session as SessionModel
from app.schemas.session import SessionCreate, SessionOut
from app.schemas.common import ResponseWrapper

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("", response_model=ResponseWrapper[SessionOut])
def create_session(payload: SessionCreate, db: Session = Depends(get_db)):
    session = SessionModel(
        id=uuid.uuid4(),
        character_id=payload.character_id,
        user_id=payload.user_id or "anonymous",
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    return ResponseWrapper(data=SessionOut(
        session_id=str(session.id),
        character_id=session.character_id,
        status=session.status,
        created_at=session.created_at,
    ))
