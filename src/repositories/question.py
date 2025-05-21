from loguru import logger
from sqlalchemy import insert
from sqlalchemy.orm import selectinload

from src.api.schemas.question import QuestionCreateSchema
from src.database.models import Question
from src.repositories.base import BaseRepository


class QuestionRepository(BaseRepository):
    model = Question

    async def create_question(self, question_data: QuestionCreateSchema):
        raw_question = await self._session.scalar(
            insert(self.model)
            .values(**question_data.model_dump())
            .options(
                selectinload(
                    self.model.answer
                )
            )
            .returning(self.model)
        )
        logger.info(f"Created new question {raw_question}")
        return raw_question.to_dto()

