from uuid import UUID

from sqlalchemy import select

from src.api.schemas.user_profile import UserProfileSchema
from src.database.models import UserProfile
from src.repositories.base import BaseRepository


class UserProfileRepository(BaseRepository):
    model = UserProfile

    async def create_user_profile(self, user_profile: UserProfileSchema):

        new_profile = await self.add(obj_data=user_profile.model_dump(exclude={"id"}))
        return new_profile.to_dto()

    async def get_user_profiles(self, user_id: UUID):
        raw_user_profiles = await self._session.scalars(
            select(self.model).where(self.model.user_id == user_id)
        )

        return [
            raw_user_profile.to_dto()
            for raw_user_profile in raw_user_profiles
        ]

    async def get_user_profile_by_id(self, user_profile_id: UUID):
        raw_user_profile = await self._session.execute(
            select(self.model).where(self.model.id == user_profile_id)
        )
        return raw_user_profile.scalars().one_or_none()