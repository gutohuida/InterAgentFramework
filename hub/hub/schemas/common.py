"""Shared response schemas."""

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    error: str


class SuccessResponse(BaseModel):
    success: bool = True
    message: str = "OK"


class StatusResponse(BaseModel):
    project_id: str
    project_name: str
    message_counts: dict
    task_counts: dict
    question_counts: dict
    agents_active: list
