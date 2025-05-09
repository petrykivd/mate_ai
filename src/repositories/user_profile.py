from src.api.schemas.user_profile import UserProfileSchema
from src.database.models import UserProfile
from src.repositories.base import BaseRepository


class UserProfileRepository(BaseRepository):
    model = UserProfile

    async def create_user_profile(self, user_profile: UserProfileSchema):

        new_profile = await self.add(obj_data=user_profile.model_dump(exclude={"id"}))
        return new_profile.to_dto()
