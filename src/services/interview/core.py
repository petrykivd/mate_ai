import asyncio
from uuid import UUID

from asyncpg import ForeignKeyViolationError
from fastapi import HTTPException
from loguru import logger

from src.api.schemas.interview import InterviewCreateSchema
from src.api.schemas.question import QuestionCreateSchema
from src.clients.gemini.client import GeminiClient
from src.repositories.interview import InterviewRepository
from src.repositories.question import QuestionRepository
from src.repositories.user_profile import UserProfileRepository
from src.services.interview.prompts import QUESTION_GENERATION_PROMPT


class InterviewService:

    def __init__(
        self,
        interview_repo: InterviewRepository,
        profile_repo: UserProfileRepository,
        question_repo: QuestionRepository,
        llm_client: GeminiClient,
    ):
        self._interview_repo = interview_repo
        self._profile_repo = profile_repo
        self._question_repo = question_repo
        self._llm_client = llm_client


    async def create_new_interview(self, interview_data: InterviewCreateSchema):
        logger.info(f"Creating new interview: {interview_data}")

        if interview_data.profile_id:
            user_profile = await self.get_profile_or_raise(interview_data.profile_id)
            interview_data.update_from_user_profile(user_profile)

        try:
            new_interview = await self._interview_repo.create_interview(interview_data=interview_data)
        except ForeignKeyViolationError as e:
            logger.error(f"Error occurred while creating interview\n"
                         f"Error: {e}")
            raise HTTPException(status_code=404, detail="User not found")

        logger.info(f"Created new interview: {new_interview}")

        question_text = await self.generate_question(interview_data)

        await self._question_repo.create_question(
            question_data=QuestionCreateSchema(
                text=question_text,
                interview_id=new_interview.id,
            )
        )

        return new_interview

    async def get_profile_or_raise(self, profile_id: UUID):
        user_profile = await self._profile_repo.get_user_profile_by_id(profile_id)
        if not user_profile:
            raise HTTPException(
                status_code=404,
                detail=f"User profile with id {profile_id} not found"
            )
        return user_profile

    async def generate_question(self, interview_data: InterviewCreateSchema):
        text, _ = await self._llm_client.send_message(
            system_prompt=self.prepare_question_prompt(interview_data),
            message="Generate 1 question"
        )
        logger.info(f"Generated question: {text[:40]}")
        return text

    @staticmethod
    def prepare_question_prompt( interview_data: InterviewCreateSchema):
        return QUESTION_GENERATION_PROMPT.format(
            job_position=interview_data.job_position,
            experience=interview_data.experience,
            tech_stack=interview_data.tech_stack,
        )