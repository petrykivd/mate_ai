from google import genai
from google.genai import types
from google.genai.types import GenerateContentResponse, FunctionCall
from loguru import logger

from src.clients.base import BaseLLMClient
from src.clients.gemini.config import get_gemini_settings
from src.services.user_profile.tools.mapper import tools_mapper


class GeminiClient(BaseLLMClient):

    def __init__(self):
        self._settings = get_gemini_settings()

    async def send_message(
        self,
        system_prompt: str,
        message: str,
        tools: list = None,
    ) -> tuple[str, any]:
        config = types.GenerateContentConfig(system_instruction=system_prompt)
        if tools:
            client_tools = types.Tool(function_declarations=tools)
            config.tools = [client_tools]

        client = genai.Client(api_key=self._settings.API_KEY)
        response = await client.aio.models.generate_content(
            model=self._settings.MODEL,
            config=config,
            contents=message,
        )
        # TODO: Improve it (create Model for LLM Response)
        result = None
        if func_call := self.get_func_call(response):
            tool = tools_mapper.get(func_call.name)
            logger.critical(f"Executing tool: {tool} with args: {func_call.args}")
            result = await tools_mapper.get(func_call.name)(**func_call.args).execute()
        return response.text, result

    @staticmethod
    def get_func_call(response: GenerateContentResponse) -> FunctionCall | None:
        logger.warning(f"Gemini response: {response}")
        if response.candidates[0].content.parts[0].function_call:
            function_call = response.candidates[0].content.parts[0].function_call
            logger.debug(f"Gemini function call found!\n{function_call}")
            return function_call

        return None


def get_gemini_client() -> GeminiClient:
    return GeminiClient()
