from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from src.api.schemas.answer import AnswerDetailSchema
from src.api.schemas.interview import InterviewDetailSchema
from src.api.schemas.user_profile import UserProfileSchema
from src.database.models.base import Base, IdCreatedAtModelMixin


class Answer(Base, IdCreatedAtModelMixin):
    __tablename__ = "answers"

    text: Mapped[str]
    score: Mapped[float] = mapped_column(nullable=True)
    feedback: Mapped[str] = mapped_column(nullable=True)

    # relations
    question_id: Mapped[UUID] = mapped_column(ForeignKey("questions.id"))



    def to_dto(self) -> AnswerDetailSchema:
        return AnswerDetailSchema(
            text=self.text,
            score=self.score,
            feedback=self.feedback,
            id=self.id,
            question_id=self.question_id,
        )

