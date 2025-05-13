from sqlalchemy.orm import Mapped, relationship

from src.api.schemas.user import UserDetailResponseSchema
from src.database.models.base import Base, IdCreatedAtModelMixin


class User(Base, IdCreatedAtModelMixin):
    __tablename__ = "users"

    fullname: Mapped[str]
    username: Mapped[str]
    password: Mapped[str]

    # relations
    profiles: Mapped[list["UserProfile"]] = relationship()
    interviews: Mapped[list["Interview"]] = relationship()

    def to_dto(self) -> UserDetailResponseSchema:
        return UserDetailResponseSchema(
            id=self.id,
            fullname=self.fullname,
            username=self.username,
        )
