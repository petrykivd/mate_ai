from sqlalchemy.orm import Mapped

from src.api.schemas.user import UserDetailResponseSchema
from src.database.models.base import Base, IdModelMixin


class User(Base, IdModelMixin):
    __tablename__ = "users"

    fullname: Mapped[str]
    username: Mapped[str]
    password: Mapped[str]

    def to_dto(self) -> UserDetailResponseSchema:
        return UserDetailResponseSchema(
            id=self.id,
            fullname=self.fullname,
            username=self.username,
        )
