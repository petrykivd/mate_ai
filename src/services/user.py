from uuid import UUID

from fastapi import HTTPException

from src.api.schemas.user import UserCreateSchema
from src.repositories.user import UserRepository


class UserService:

    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    async def create_new_user(self, user: UserCreateSchema):
        return await self._user_repo.create_user(user=user)

    async def get_user_by_id(self, user_id: UUID):
        user = await self._user_repo.get_user_by_id(user_id=user_id)
        # TODO: Implement your own exception (usernotfoundexception)
        if not user:
            raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
