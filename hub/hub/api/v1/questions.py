"""Question endpoints — POST/GET/GET{id}/PATCH."""

from datetime import datetime, timezone
from typing import List, Optional, Tuple

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...auth import get_project
from ...db.engine import get_session
from ...db.models import Question
from ...schemas.questions import QuestionAnswer, QuestionCreate, QuestionResponse
from ...sse import sse_manager
from ...utils import short_id

router = APIRouter(prefix="/questions", tags=["questions"])


@router.post("", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
async def ask_question(
    body: QuestionCreate,
    project: Tuple[str, str] = Depends(get_project),
    session: AsyncSession = Depends(get_session),
):
    project_id, _ = project
    q_id = f"q-{short_id()}"
    question = Question(
        id=q_id,
        project_id=project_id,
        from_agent=body.from_agent,
        question=body.question,
        blocking=body.blocking,
    )
    session.add(question)
    await session.commit()
    await session.refresh(question)
    await sse_manager.broadcast(
        project_id, "question_asked",
        {"id": q_id, "from_agent": body.from_agent, "blocking": body.blocking}
    )
    return question


@router.get("", response_model=List[QuestionResponse])
async def list_questions(
    answered: Optional[bool] = Query(None),
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    project: Tuple[str, str] = Depends(get_project),
    session: AsyncSession = Depends(get_session),
):
    project_id, _ = project
    q = select(Question).where(Question.project_id == project_id)
    if answered is not None:
        q = q.where(Question.answered == answered)
    q = q.order_by(Question.created_at).offset(offset).limit(limit)
    result = await session.execute(q)
    return result.scalars().all()


@router.get("/{question_id}", response_model=QuestionResponse)
async def get_question(
    question_id: str,
    project: Tuple[str, str] = Depends(get_project),
    session: AsyncSession = Depends(get_session),
):
    project_id, _ = project
    question = await session.get(Question, question_id)
    if question is None or question.project_id != project_id:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@router.patch("/{question_id}", response_model=QuestionResponse)
async def answer_question(
    question_id: str,
    body: QuestionAnswer,
    project: Tuple[str, str] = Depends(get_project),
    session: AsyncSession = Depends(get_session),
):
    project_id, _ = project
    question = await session.get(Question, question_id)
    if question is None or question.project_id != project_id:
        raise HTTPException(status_code=404, detail="Question not found")
    question.answer = body.answer
    question.answered = True
    question.answered_at = datetime.now(timezone.utc)
    await session.commit()
    await session.refresh(question)
    await sse_manager.broadcast(
        project_id, "question_answered",
        {"id": question_id, "answer": body.answer}
    )
    return question
