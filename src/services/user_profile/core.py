from uuid import UUID

from src.api.schemas.user_profile import UserProfileCreateSchema, UserProfileSchema
from src.clients.gemini.client import GeminiClient
from src.repositories.user_profile import UserProfileRepository
from src.services.user_profile.prompts import PROFILE_GENERATE_SYSTEM_PROMPT
from src.services.user_profile.tools.tool_definitions import SaveUserProfile
from src.utils.pdf_reader import read_pdf_text_from_upload_file


class UserProfileService:

    def __init__(self, llm_client: GeminiClient, profile_repo: UserProfileRepository):
        self._llm_client = llm_client
        self._profile_repo = profile_repo


    async def generate_user_profile(self, profile_data: UserProfileCreateSchema):
        cv_text = await read_pdf_text_from_upload_file(
            upload_file=profile_data.cv_file
        )

        text, tool_result = await self._llm_client.send_message(
            system_prompt=PROFILE_GENERATE_SYSTEM_PROMPT,
            message=f"Here is user's CV text:\n {cv_text}\n"
                    f"Also, here is user's ID: {profile_data.user_id}\n",
            tools=[SaveUserProfile.to_function_definition()]
        )

        if tool_result:
            user_profile = await self._profile_repo.create_user_profile(
                user_profile=tool_result
            )

            return user_profile

        raise RuntimeError("Failed to generate user profile")

    async def get_user_profiles(self, user_id: UUID) -> list[UserProfileSchema]:

        return await self._profile_repo.get_user_profiles(user_id)
