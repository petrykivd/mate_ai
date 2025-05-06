from typing import Annotated, Dict
from uuid import UUID

from pydantic import BaseModel, Field


class UserCreateSchema(BaseModel):
    fullname: str
    username: str
    password: str


class UserUpdateSchema(BaseModel):
    fullname: Annotated[str | None, Field()] = None
    username: Annotated[str | None, Field()] = None
    password: Annotated[str | None, Field()] = None


class UserCreateResponseSchema(BaseModel):
    id: UUID

class UserDetailResponseSchema(BaseModel):
    id: UUID
    fullname: str
    username: str

class UserListResponseSchema(BaseModel):
    users: list[UserDetailResponseSchema]
