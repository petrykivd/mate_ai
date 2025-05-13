from src.api.schemas.question import QuestionCreateSchema
from src.database.models import Question
from src.repositories.base import BaseRepository


class QuestionRepository(BaseRepository):
    model = Question

    async def create_question(self, question_data: QuestionCreateSchema):
        raw_question = await self.add(obj_data=question_data.model_dump())
        return raw_question.to_dto()
