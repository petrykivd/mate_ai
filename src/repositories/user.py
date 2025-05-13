from uuid import UUID

from src.api.schemas.user import (
    UserCreateSchema,
    UserDetailResponseSchema,
)
from src.database.models.user.user import User
from src.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    model = User


    async def create_user(self, user: UserCreateSchema) -> UserDetailResponseSchema:
        new_user = await self.add(obj_data=user.model_dump())

        return new_user.to_dto()

    async def get_user_by_id(self, user_id: UUID) -> UserDetailResponseSchema | None:
        user = await self.get(obj_id=user_id)
        if user:
            return user.to_dto()

        raise UserNotFoundException(user_id)
