from uuid import UUID

from fastapi import APIRouter

from src.api.dependencies import InterviewServiceDep
from src.api.schemas.answer import AnswerCreateSchema
from src.api.schemas.interview import InterviewCreateSchema, \
    InterviewFinishResponseSchema

router = APIRouter(tags=["Interviews"], prefix="/interviews")

@router.post("")
async def create_interview(
    interview_data: InterviewCreateSchema,
    interview_service: InterviewServiceDep
):
    interview = await interview_service.create_new_interview(interview_data)

    return interview

@router.get("/{interview_id}")
async def get_interview(
    interview_id: UUID,
    interview_service: InterviewServiceDep
):
    interview = await interview_service.get_interview_by_id(interview_id)

    return interview


@router.post("/{interview_id}/questions/answer")
async def answer_question(
    question_data: AnswerCreateSchema,
    interview_id: UUID,
    interview_service: InterviewServiceDep
):
    return await interview_service.create_answer_for_question(question_data, interview_id)

@router.post("/{interview_id}/finish", response_model=InterviewFinishResponseSchema)
async def finish_interview(
    interview_id: UUID,
    interview_service: InterviewServiceDep
):
    feedback = await interview_service.finish_interview(interview_id)

    return InterviewFinishResponseSchema(
        feedback=feedback,
        id=interview_id,
    )
