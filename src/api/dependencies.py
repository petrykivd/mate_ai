from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.core.engine import get_async_session
from src.repositories.user import UserRepository
from src.services.user import UserService

AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]


def get_user_repository(
    session: AsyncSessionDep
) -> UserRepository:
    return UserRepository(session=session)

UserRepoDep = Annotated[UserRepository, Depends(get_user_repository)]

def get_user_service(
    user_repo: UserRepoDep
):
    return UserService(user_repo=user_repo)

UserServiceDep = Annotated[UserService, Depends(get_user_service)]
