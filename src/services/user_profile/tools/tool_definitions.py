from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from src.api.schemas.user_profile import UserProfileSchema


class SaveUserProfile(BaseModel):
    """
        Use this tool for save user profile
    """

    user_id: str = Field(description="User id in UUID format")

    job_position: Optional[str] = Field(
        description="Job position of the user"
                    " (e.g. Software Engineer, Data Scientist, etc.)",
        default=None,
    )
    experience: Optional[float] = Field(
        description="Experience of the user (in years)"
                    "(e.g 0.5, 1, 5, 4,2, etc.)",
        default=None,
    )
    tech_stack: Optional[str] = Field(
        description="Tech stack of the user"
                    "(e.g. "
                    "Python Backend: FastAPI, SQLAlchemy, Alembic, SOLID, Celery, Docker."
                    "JavaScript Frontend: React, React-Admin, Material-UI."
                    "Java Backend: Spring, JVM"
                    ")",
        default=None,
    )

    async def execute(self):
        user_profile = UserProfileSchema(
            user_id=UUID(self.user_id),
            job_position=self.job_position,
            experience=self.experience,
            tech_stack=self.tech_stack
        )

        return user_profile

    @classmethod
    def to_function_definition(cls):
        return {
            "name": cls.__name__,
            "description": cls.__doc__,
            "parameters": cls.model_json_schema(),
        }
