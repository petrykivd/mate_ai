from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.clients.gemini.client import GeminiClient, get_gemini_client
from src.database.core.engine import get_async_session
from src.repositories.interview import InterviewRepository
from src.repositories.question import QuestionRepository
from src.repositories.user import UserRepository
from src.repositories.user_profile import UserProfileRepository
from src.services.interview.core import InterviewService
from src.services.user import UserService
from src.services.user_profile.core import UserProfileService

AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]


def get_user_repository(
    session: AsyncSessionDep
) -> UserRepository:
    return UserRepository(session=session)
UserRepoDep = Annotated[UserRepository, Depends(get_user_repository)]


def get_user_profile_repository(
    session: AsyncSessionDep
) -> UserProfileRepository:
    return UserProfileRepository(session=session)
UserProfileRepoDep = Annotated[UserProfileRepository, Depends(get_user_profile_repository)]


def get_interview_repository(
    session: AsyncSessionDep
):
    return InterviewRepository(session=session)
InterviewRepoDep = Annotated[InterviewRepository, Depends(get_interview_repository)]


def get_question_repository(
    session: AsyncSessionDep
):
    return QuestionRepository(session=session)
QuestionRepoDep = Annotated[QuestionRepository, Depends(get_question_repository)]

def get_user_service(
    user_repo: UserRepoDep
):
    return UserService(user_repo=user_repo)
UserServiceDep = Annotated[UserService, Depends(get_user_service)]


GeminiClientDep = Annotated[GeminiClient, Depends(get_gemini_client)]
def get_user_profile_service(
    gemini_client: GeminiClientDep,
    profile_repo: UserProfileRepoDep
):
    return UserProfileService(llm_client=gemini_client, profile_repo=profile_repo)
UserProfileServiceDep = Annotated[UserProfileService, Depends(get_user_profile_service)]


def get_interview_service(
    interview_repo: InterviewRepoDep,
    profile_repo: UserProfileRepoDep,
    question_repo: QuestionRepoDep,
    gemini_client: GeminiClientDep,
):
    return InterviewService(
        interview_repo=interview_repo,
        question_repo=question_repo,
        profile_repo=profile_repo,
        llm_client=gemini_client,
    )
InterviewServiceDep = Annotated[InterviewService, Depends(get_interview_service)]
