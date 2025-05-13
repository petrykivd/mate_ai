from uuid import UUID

from pydantic import BaseModel


class QuestionCreateSchema(BaseModel):
    text: str
    interview_id: UUID

class QuestionDetailSchema(BaseModel):
    id: UUID
    text: str
    interview_id: UUID
