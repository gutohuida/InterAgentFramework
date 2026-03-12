"""Task schemas."""

from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    description: str = ""
    status: str = "pending"
    priority: str = "medium"
    assignee: Optional[str] = None
    assigner: Optional[str] = None
    requirements: Optional[List[Any]] = None
    acceptance_criteria: Optional[List[Any]] = None
    deliverables: Optional[List[Any]] = None
    notes: Optional[Any] = None
    # Allow id/created_at to be passed from CLI format
    id: Optional[str] = None
    created_at: Optional[str] = None


class TaskUpdate(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
    assignee: Optional[str] = None
    description: Optional[str] = None
    notes: Optional[Any] = None


class TaskResponse(BaseModel):
    id: str
    project_id: str
    title: str
    description: str
    status: str
    priority: str
    assignee: Optional[str]
    assigner: Optional[str]
    created_at: datetime
    updated: datetime
    requirements: Optional[Any]
    acceptance_criteria: Optional[Any]
    deliverables: Optional[Any]
    notes: Optional[Any]

    model_config = {"from_attributes": True}
