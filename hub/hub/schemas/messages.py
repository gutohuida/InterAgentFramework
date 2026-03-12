"""Message schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class MessageCreate(BaseModel):
    # JSON uses "from"/"to"; Python model uses sender/recipient
    sender: str = Field(alias="from")
    recipient: str = Field(alias="to")
    subject: Optional[str] = None
    content: str
    type: str = "message"
    task_id: Optional[str] = None
    # Allow "id" and "timestamp" to be passed in for compatibility with existing CLI format
    id: Optional[str] = None
    timestamp: Optional[str] = None

    model_config = {"populate_by_name": True}


class MessageResponse(BaseModel):
    id: str
    project_id: str
    sender: str = Field(serialization_alias="from")
    recipient: str = Field(serialization_alias="to")
    subject: Optional[str]
    content: str
    type: str
    timestamp: datetime
    read: bool
    read_at: Optional[datetime]
    task_id: Optional[str]

    model_config = {"populate_by_name": True, "from_attributes": True}
