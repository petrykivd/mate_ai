from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from src.api.schemas.interview import InterviewDetailSchema
from src.api.schemas.question import QuestionDetailSchema
from src.api.schemas.user_profile import UserProfileSchema
from src.database.models.base import Base, IdCreatedAtModelMixin


class Question(Base, IdCreatedAtModelMixin):
    __tablename__ = "questions"

    text: Mapped[str]
    interview_id: Mapped[UUID] = mapped_column(ForeignKey("interviews.id"))


    def to_dto(self) -> QuestionDetailSchema:
        return QuestionDetailSchema(
            id=self.id,
            text=self.text,
            interview_id=self.interview_id,
        )
