from uuid import UUID

from fastapi import APIRouter, UploadFile, File

from src.api.dependencies import UserProfileServiceDep
from src.api.schemas.user_profile import UserProfileCreateSchema

router = APIRouter(tags=["User profiles"], prefix="/user-profiles")

@router.post("")
async def generate_user_profile(
    user_id: UUID,
    profile_service: UserProfileServiceDep,
    cv_file: UploadFile = File(...),
):
    profile_data = UserProfileCreateSchema(
        user_id=user_id,
        cv_file=cv_file
    )

    result = await profile_service.generate_user_profile(profile_data)


    return {"result": result}
