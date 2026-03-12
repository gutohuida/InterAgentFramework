"""Tests for SSE manager."""

import asyncio
import pytest
from hub.sse import SSEManager


@pytest.mark.asyncio
async def test_subscribe_broadcast_unsubscribe():
    manager = SSEManager()
    q = manager.subscribe("proj-test")
    await manager.broadcast("proj-test", "task_created", {"id": "task-abc"})
    msg = q.get_nowait()
    assert "task_created" in msg
    assert "task-abc" in msg
    manager.unsubscribe("proj-test", q)
    assert "proj-test" not in manager._subscribers


@pytest.mark.asyncio
async def test_broadcast_no_subscribers():
    manager = SSEManager()
    # Should not raise even with no subscribers
    await manager.broadcast("proj-none", "message_created", {"id": "msg-xyz"})
