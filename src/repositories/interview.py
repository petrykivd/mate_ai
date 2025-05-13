from src.api.schemas.interview import InterviewCreateSchema
from src.database.models import Interview
from src.repositories.base import BaseRepository


class InterviewRepository(BaseRepository):
    model = Interview

    async def create_interview(self, interview_data: InterviewCreateSchema):
        raw_interview = await self.add(
            obj_data=interview_data.model_dump(exclude={"profile_id"})
        )

        dto = raw_interview.to_dto()
        return dto
