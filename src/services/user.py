from src.api.schemas.user import UserCreateSchema
from src.repositories.user import UserRepository


class UserService:

    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    async def create_new_user(self, user: UserCreateSchema):
        return await self._user_repo.create_user(user=user)
