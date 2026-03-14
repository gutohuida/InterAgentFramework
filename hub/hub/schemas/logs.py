"""Event log schemas."""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


class EventLogResponse(BaseModel):
    id: str
    project_id: str
    event_type: str
    agent: Optional[str]
    data: Optional[Any]
    timestamp: datetime

    model_config = {"from_attributes": True}
