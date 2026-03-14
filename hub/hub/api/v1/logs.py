"""GET /api/v1/logs — persistent event log endpoint."""

from datetime import datetime
from typing import List, Optional, Tuple

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...auth import get_project
from ...db.engine import get_session
from ...db.models import EventLog
from ...schemas.logs import EventLogResponse

router = APIRouter(prefix="/logs", tags=["logs"])


@router.get("", response_model=List[EventLogResponse])
async def list_logs(
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    agent: Optional[str] = Query(None),
    event_type: Optional[str] = Query(None),
    since: Optional[str] = Query(None),
    project: Tuple[str, str] = Depends(get_project),
    session: AsyncSession = Depends(get_session),
):
    project_id, _ = project
    q = select(EventLog).where(EventLog.project_id == project_id)
    if agent:
        q = q.where(EventLog.agent == agent)
    if event_type:
        q = q.where(EventLog.event_type == event_type)
    if since:
        try:
            since_dt = datetime.fromisoformat(since)
            q = q.where(EventLog.timestamp > since_dt)
        except ValueError:
            pass
    q = q.order_by(EventLog.timestamp.asc()).offset(offset).limit(limit)
    result = await session.execute(q)
    return result.scalars().all()
