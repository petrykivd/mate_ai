from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from src.api.schemas.interview import InterviewDetailSchema
from src.database.models.base import Base, IdCreatedAtModelMixin


class Interview(Base, IdCreatedAtModelMixin):
    __tablename__ = "interviews"

    title: Mapped[str] = mapped_column()
    # TODO: remove this fields and replace with interview_profile_id
    job_position: Mapped[str] = mapped_column()
    experience: Mapped[float] = mapped_column()
    # TODO: Can be improved by using JSON field
    tech_stack: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)
    feedback: Mapped[str] = mapped_column(nullable=True)

    # relations
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))

    questions: Mapped[list["Question"]] = relationship()


    def to_dto(self):
        return InterviewDetailSchema(
            id=self.id,
            feedback=self.feedback,
            is_active=self.is_active,
            title=self.title,
            tech_stack=self.tech_stack,
            job_position=self.job_position,
            experience=self.experience,
            user_id=self.user_id,
            questions=[question.to_dto() for question in self.questions]
        )
