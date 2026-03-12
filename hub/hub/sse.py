"""SSE fan-out manager.

One SSEManager instance is shared across all requests.
Agents subscribe by calling .subscribe(project_id), which returns a queue.
After every write operation, call .broadcast(project_id, event_type, data).
"""

import asyncio
import json
from typing import Any, Dict, List


class SSEManager:
    def __init__(self) -> None:
        # project_id -> list of asyncio.Queue
        self._subscribers: Dict[str, List[asyncio.Queue]] = {}

    def subscribe(self, project_id: str) -> asyncio.Queue:
        """Register a new SSE subscriber for a project. Returns the queue."""
        q: asyncio.Queue = asyncio.Queue(maxsize=256)
        self._subscribers.setdefault(project_id, []).append(q)
        return q

    def unsubscribe(self, project_id: str, queue: asyncio.Queue) -> None:
        """Remove a subscriber queue (called on client disconnect)."""
        subscribers = self._subscribers.get(project_id, [])
        try:
            subscribers.remove(queue)
        except ValueError:
            pass
        if not subscribers:
            self._subscribers.pop(project_id, None)

    async def broadcast(self, project_id: str, event_type: str, data: Any) -> None:
        """Push an SSE event to all subscribers of a project."""
        payload = json.dumps(data, default=str)
        message = f"event: {event_type}\ndata: {payload}\n\n"
        for q in list(self._subscribers.get(project_id, [])):
            try:
                q.put_nowait(message)
            except asyncio.QueueFull:
                pass  # Slow consumer — drop event rather than block


sse_manager = SSEManager()
