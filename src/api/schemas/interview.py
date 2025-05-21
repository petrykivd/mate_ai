from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field, model_validator

from src.api.schemas.question import QuestionDetailSchema
from src.api.schemas.user_profile import UserProfileSchema

# TODO: Use BaseSchema instead of BaseModel

class InterviewCreateSchema(BaseModel):
    title: Annotated[str | None, Field()] = None
    job_position: Annotated[str | None, Field()] = None
    experience: Annotated[float | None, Field()] = None
    tech_stack: Annotated[str | None, Field()] = None
    user_id: Annotated[UUID, Field()]
    profile_id: Annotated[UUID | None, Field()] = None

    @model_validator(mode='after')
    def set_title_if_none(self) -> 'InterviewCreateSchema':
        if not self.title:
            self.set_title()
        return self

    @model_validator(mode='after')
    def check_profile_or_args(self) -> 'InterviewCreateSchema':
        if not self.profile_id:
            if not self.job_position or not self.experience or not self.tech_stack:
                raise ValueError("You must provide either profile_id or job_position, experience and tech_stack")

        return self

    def update_from_user_profile(self, user_profile: UserProfileSchema):
        self.job_position = user_profile.job_position
        self.experience = user_profile.experience
        self.tech_stack = user_profile.tech_stack
        self.set_title()

    def set_title(self):
        self.title = f"Interview {self.job_position} - {self.experience} y."

class InterviewDetailSchema(BaseModel):
    id: UUID
    is_active: bool
    title: str
    feedback: Annotated[str | None, Field()] = None
    job_position: str
    experience: float
    tech_stack: str
    user_id: UUID
    questions: list[QuestionDetailSchema]


class InterviewFinishResponseSchema(BaseModel):
    id: UUID
    feedback: str
