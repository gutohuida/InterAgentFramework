"""GET /api/v1/events — SSE stream."""

import asyncio
from typing import AsyncGenerator, Tuple

from fastapi import APIRouter, Depends, Request
from sse_starlette.sse import EventSourceResponse

from ...auth import get_project
from ...sse import sse_manager

router = APIRouter(prefix="/events", tags=["events"])


@router.get("")
async def event_stream(
    request: Request,
    project: Tuple[str, str] = Depends(get_project),
):
    project_id, _ = project
    queue = sse_manager.subscribe(project_id)

    async def generator() -> AsyncGenerator[str, None]:
        try:
            yield "data: connected\n\n"
            while True:
                if await request.is_disconnected():
                    break
                try:
                    message = await asyncio.wait_for(queue.get(), timeout=30)
                    yield message
                except asyncio.TimeoutError:
                    # Send keepalive comment
                    yield ": keepalive\n\n"
        finally:
            sse_manager.unsubscribe(project_id, queue)

    return EventSourceResponse(generator())
