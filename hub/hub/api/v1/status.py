"""GET /api/v1/status — project health snapshot."""

from datetime import datetime, timedelta, timezone
from typing import Tuple

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ...auth import get_project
from ...db.engine import get_session
from ...db.models import Message, Question, Task
from ...schemas.common import StatusResponse

router = APIRouter(prefix="/status", tags=["status"])


@router.get("", response_model=StatusResponse)
async def get_status(
    project: Tuple[str, str] = Depends(get_project),
    session: AsyncSession = Depends(get_session),
):
    project_id, project_name = project

    # Message counts
    total_msgs = await session.scalar(
        select(func.count()).select_from(Message).where(Message.project_id == project_id)
    )
    pending_msgs = await session.scalar(
        select(func.count()).select_from(Message).where(
            Message.project_id == project_id, Message.read == False  # noqa: E712
        )
    )

    # Task counts by status
    task_rows = await session.execute(
        select(Task.status, func.count()).where(Task.project_id == project_id).group_by(Task.status)
    )
    task_counts = {row[0]: row[1] for row in task_rows}

    # Question counts
    total_qs = await session.scalar(
        select(func.count()).select_from(Question).where(Question.project_id == project_id)
    )
    unanswered_qs = await session.scalar(
        select(func.count()).select_from(Question).where(
            Question.project_id == project_id, Question.answered == False  # noqa: E712
        )
    )

    # Active agents: senders of messages or assignees of active tasks in last 24 h
    cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
    sender_rows = await session.execute(
        select(Message.sender).distinct().where(
            Message.project_id == project_id, Message.timestamp >= cutoff
        )
    )
    senders = {r[0] for r in sender_rows}
    assignee_rows = await session.execute(
        select(Task.assignee).distinct().where(
            Task.project_id == project_id,
            Task.assignee.isnot(None),
            Task.status.in_(["in_progress", "assigned", "pending"]),
        )
    )
    assignees = {r[0] for r in assignee_rows if r[0]}
    agents_active = sorted(senders | assignees)

    return StatusResponse(
        project_id=project_id,
        project_name=project_name,
        message_counts={"pending": pending_msgs or 0, "total": total_msgs or 0},
        task_counts=task_counts,
        question_counts={"unanswered": unanswered_qs or 0, "total": total_qs or 0},
        agents_active=agents_active,
    )
