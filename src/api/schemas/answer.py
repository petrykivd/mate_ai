from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field


class AnswerCreateSchema(BaseModel):
    text: str
    question_id: Annotated[UUID | None, Field()] = None

class AnswerDetailSchema(BaseModel):
    id: UUID
    text: str
    score: Annotated[float | None, Field()]
    feedback: Annotated[str | None, Field()]
    question_id: UUID