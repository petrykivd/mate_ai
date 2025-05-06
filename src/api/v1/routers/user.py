from uuid import UUID

from fastapi import APIRouter

from src.api.dependencies import UserServiceDep
from src.api.schemas.user import (
    UserCreateSchema,
    UserUpdateSchema,
    UserCreateResponseSchema, UserDetailResponseSchema,
)

router = APIRouter(tags=["Users"], prefix="/users")


@router.post("", response_model=UserCreateResponseSchema)
async def create_user(
    user_data: UserCreateSchema,
    user_service: UserServiceDep
):
    new_user = await user_service.create_new_user(user_data)
    return new_user.id

@router.get("")
async def get_all_users(
):
    pass

@router.get("/{user_id}", response_model=UserDetailResponseSchema)
async def get_user_by_id(
    user_id: UUID,
):
    pass

@router.patch("/{user_id}")
async def partial_update_user(
    user_id: UUID,
    new_user_data: UserUpdateSchema
):
    pass

@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: UUID,
):
    pass