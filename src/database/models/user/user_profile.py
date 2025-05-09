from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from src.api.schemas.user_profile import UserProfileSchema
from src.database.models.base import Base, IdCreatedAtModelMixin


class UserProfile(Base, IdCreatedAtModelMixin):
    __tablename__ = "user_profiles"

    job_position: Mapped[str] = mapped_column(nullable=True)
    experience: Mapped[float] = mapped_column(nullable=True)
    # TODO: Can be improved by using JSON field
    tech_stack: Mapped[str] = mapped_column(nullable=True)

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))


    def to_dto(self):
        return UserProfileSchema(
            id=self.id,
            user_id=self.user_id,
            job_position=self.job_position,
            experience=self.experience,
            tech_stack=self.tech_stack,
        )
