"""Question schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class QuestionCreate(BaseModel):
    from_agent: str
    question: str
    blocking: bool = False


class QuestionAnswer(BaseModel):
    answer: str


class QuestionResponse(BaseModel):
    id: str
    project_id: str
    from_agent: str
    question: str
    answer: Optional[str]
    answered: bool
    blocking: bool
    created_at: datetime
    answered_at: Optional[datetime]

    model_config = {"from_attributes": True}
