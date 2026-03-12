"""Message endpoints — POST/GET/PATCH."""

from datetime import datetime, timezone
from typing import List, Optional, Tuple
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...auth import get_project
from ...db.engine import get_session
from ...db.models import Message
from ...schemas.common import SuccessResponse
from ...schemas.messages import MessageCreate, MessageResponse
from ...sse import sse_manager

router = APIRouter(prefix="/messages", tags=["messages"])


def _uuid6() -> str:
    return str(uuid.uuid4())[:8]


@router.post("", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def create_message(
    body: MessageCreate,
    project: Tuple[str, str] = Depends(get_project),
    session: AsyncSession = Depends(get_session),
):
    project_id, _ = project
    msg_id = body.id or f"msg-{_uuid6()}"
    msg = Message(
        id=msg_id,
        project_id=project_id,
        sender=body.sender,
        recipient=body.recipient,
        subject=body.subject,
        content=body.content,
        type=body.type,
        timestamp=datetime.fromisoformat(body.timestamp) if body.timestamp else datetime.now(timezone.utc),
        task_id=body.task_id,
    )
    session.add(msg)
    await session.commit()
    await session.refresh(msg)
    await sse_manager.broadcast(project_id, "message_created", _msg_dict(msg))
    return msg


@router.get("", response_model=List[MessageResponse])
async def list_messages(
    agent: Optional[str] = Query(None),
    project: Tuple[str, str] = Depends(get_project),
    session: AsyncSession = Depends(get_session),
):
    project_id, _ = project
    q = select(Message).where(Message.project_id == project_id, Message.read == False)  # noqa: E712
    if agent:
        q = q.where(Message.recipient == agent)
    q = q.order_by(Message.timestamp)
    result = await session.execute(q)
    return result.scalars().all()


@router.patch("/{message_id}/read", response_model=SuccessResponse)
async def mark_read(
    message_id: str,
    project: Tuple[str, str] = Depends(get_project),
    session: AsyncSession = Depends(get_session),
):
    project_id, _ = project
    msg = await session.get(Message, message_id)
    if msg is None or msg.project_id != project_id:
        raise HTTPException(status_code=404, detail="Message not found")
    msg.read = True
    msg.read_at = datetime.now(timezone.utc)
    await session.commit()
    await sse_manager.broadcast(project_id, "message_read", {"id": message_id})
    return SuccessResponse(message="Message marked as read")


def _msg_dict(msg: Message) -> dict:
    return {
        "id": msg.id,
        "from": msg.sender,
        "to": msg.recipient,
        "subject": msg.subject,
        "type": msg.type,
        "timestamp": msg.timestamp.isoformat() if msg.timestamp else None,
    }
