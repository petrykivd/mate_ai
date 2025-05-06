from src.api.schemas.user import (
    UserCreateSchema,
    UserDetailResponseSchema,
)
from src.database.models.user import User
from src.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    model = User


    async def create_user(self, user: UserCreateSchema) -> UserDetailResponseSchema:
        new_user = await self.add(obj_data=user.model_dump())

        return new_user.to_dto()
