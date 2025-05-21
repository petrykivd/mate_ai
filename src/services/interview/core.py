from uuid import UUID

from asyncpg import ForeignKeyViolationError
from fastapi import HTTPException
from loguru import logger

from src.api.schemas.answer import AnswerCreateSchema
from src.api.schemas.interview import InterviewCreateSchema, InterviewDetailSchema
from src.api.schemas.question import QuestionCreateSchema
from src.clients.gemini.client import GeminiClient
from src.repositories.answer import AnswerRepository
from src.repositories.interview import InterviewRepository
from src.repositories.question import QuestionRepository
from src.repositories.user_profile import UserProfileRepository
from src.services.interview.prompts import QUESTION_GENERATION_PROMPT, \
    ANSWER_RATING_PROMPT, INTERVIEW_RATING_PROMPT
from src.services.interview.tools.tool_definitions import SaveAnswerRate


class InterviewService:

    def __init__(
        self,
        interview_repo: InterviewRepository,
        profile_repo: UserProfileRepository,
        question_repo: QuestionRepository,
        answer_repo: AnswerRepository,
        llm_client: GeminiClient,
    ):
        self._interview_repo = interview_repo
        self._profile_repo = profile_repo
        self._question_repo = question_repo
        self._answer_repo = answer_repo
        self._llm_client = llm_client

    async def create_new_interview(self, interview_data: InterviewCreateSchema):
        logger.info(f"Creating new interview: {interview_data}")

        if interview_data.profile_id:
            user_profile = await self.get_profile_or_raise(interview_data.profile_id)
            interview_data.update_from_user_profile(user_profile)

        try:
            new_interview = await self._interview_repo.create_interview(
                interview_data=interview_data)
        except ForeignKeyViolationError as e:
            logger.error(f"Error occurred while creating interview\n"
                         f"Error: {e}")
            raise HTTPException(status_code=404, detail="User not found")

        logger.info(f"Created new interview: {new_interview}")

        await self.create_question(new_interview, is_first=True)

        return new_interview

    async def finish_interview(self, interview_id: UUID) -> str:
        interview_info = await self.get_interview_by_id(interview_id)
        if not interview_info.is_active:
            raise HTTPException(
                status_code=400,
                detail=f"Interview with id {interview_id} is already finished"
            )
        feedback = await self.rate_interview(interview_info)
        await self._interview_repo.update(
            obj_id=interview_id,
            obj_data={
                "is_active": False,
                "feedback": feedback,
            }
        )

        return feedback

    async def create_question(
        self,
        interview_data: InterviewCreateSchema | InterviewDetailSchema,
        is_first: bool = False,
    ):
        question_text = await self._generate_question(interview_data, is_first=is_first)
        logger.info(
            f"Generated question for interview {interview_data.id}: {question_text}"
        )

        await self._question_repo.create_question(
            question_data=QuestionCreateSchema(
                text=question_text,
                interview_id=interview_data.id,
            )
        )

    async def get_interview_by_id(self, interview_id: UUID):
        interview = await self._interview_repo.get_interview_by_id(interview_id)
        if not interview:
            raise HTTPException(
                status_code=404,
                detail=f"Interview with id {interview_id} not found"
            )
        return interview

    async def get_profile_or_raise(self, profile_id: UUID):
        user_profile = await self._profile_repo.get_user_profile_by_id(profile_id)
        if not user_profile:
            raise HTTPException(
                status_code=404,
                detail=f"User profile with id {profile_id} not found"
            )
        return user_profile

    async def _generate_question(
        self,
        interview_data: InterviewCreateSchema | InterviewDetailSchema,
        is_first: bool = False,
    ):
        system_prompt = self.prepare_question_prompt(interview_data)
        if is_first:
            system_prompt = self.prepare_first_question_prompt(interview_data)

        text, _ = await self._llm_client.send_message(
            system_prompt=system_prompt,
            message="Generate 1 question"
        )
        logger.info(f"Generated question: {text[:40]}")
        return text

    async def create_answer_for_question(self, answer_data: AnswerCreateSchema,
                                         interview_id: UUID):
        await self._answer_repo.create_answer(answer_data=answer_data)
        interview_info = await self.get_interview_by_id(interview_id)
        rated_answer = await self.rate_answer(interview_info)
        await self.create_question(interview_info)

        return rated_answer

    async def rate_answer(self, interview_info: InterviewDetailSchema):
        _, answer_rate = await self._llm_client.send_message(
            system_prompt=ANSWER_RATING_PROMPT,
            message=f"{interview_info.model_dump()}"
                    f"You should rate the last answer and save result.",
            tools=[SaveAnswerRate.to_function_definition()]
        )
        logger.info(f"Rated answer: {answer_rate}")

        rated_answer = await self._answer_repo.update_answer(
            answer_id=answer_rate.pop("answer_id"),
            new_answer_data=answer_rate,
        )

        return rated_answer

    async def rate_interview(self, interview_info: InterviewDetailSchema):
        feedback, _ = await self._llm_client.send_message(
            system_prompt=INTERVIEW_RATING_PROMPT,
            message=f"{interview_info.model_dump()}"
                    f"You should rate the interview and return result",
        )
        logger.info(f"Rated interview: {feedback}")
        return feedback

    @staticmethod
    def prepare_first_question_prompt(interview_data: InterviewCreateSchema):
        return QUESTION_GENERATION_PROMPT.format(
            job_position=interview_data.job_position,
            experience=interview_data.experience,
            tech_stack=interview_data.tech_stack,
        )

    @staticmethod
    def prepare_question_prompt(interview_data: InterviewDetailSchema):
        return QUESTION_GENERATION_PROMPT.format(
            job_position=interview_data.job_position,
            experience=interview_data.experience,
            tech_stack=interview_data.tech_stack,
            questions_and_answers=interview_data.questions,
        )
