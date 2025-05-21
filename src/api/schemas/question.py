from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field

from src.api.schemas.answer import AnswerDetailSchema


class QuestionCreateSchema(BaseModel):
    text: str
    interview_id: UUID

class QuestionDetailSchema(BaseModel):
    id: UUID
    text: str
    answer: Annotated[AnswerDetailSchema | None, Field()] = None
    interview_id: UUID
