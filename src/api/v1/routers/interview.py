from fastapi import APIRouter

from src.api.dependencies import InterviewServiceDep
from src.api.schemas.interview import InterviewCreateSchema

router = APIRouter(tags=["Interviews"], prefix="/interviews")

@router.post("")
async def create_interview(
    interview_data: InterviewCreateSchema,
    interview_service: InterviewServiceDep
):
    interview = await interview_service.create_new_interview(interview_data)

    return interview
