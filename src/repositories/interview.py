from uuid import UUID

from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.api.schemas.interview import InterviewCreateSchema
from src.database.models import Interview, Question
from src.repositories.base import BaseRepository


class InterviewRepository(BaseRepository):
    model = Interview

    async def create_interview(self, interview_data: InterviewCreateSchema):
        logger.info(f"Creating interview: {interview_data}")
        raw_interview = await self.add(
            obj_data=interview_data.model_dump(exclude={"profile_id"})
        )

        dto = raw_interview.to_dto()
        return dto

    async def get_interview_by_id(self, interview_id: UUID):
        logger.info(f"Getting interview by id: {interview_id}")
        raw_interview = await self._session.execute(
            select(self.model)
            .where(self.model.id == interview_id)
            .options(
                selectinload(
                    self.model.questions
                ).selectinload(
                    Question.answer
                )
            )
        )
        return raw_interview.scalars().one_or_none().to_dto()
