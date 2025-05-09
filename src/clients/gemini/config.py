from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class GeminiSettings(BaseSettings):
    API_KEY: str
    MODEL: str = "gemini-2.0-flash"

    model_config = SettingsConfigDict(
        env_prefix='GEMINI_',
        env_file="./.env",
        extra='ignore'
    )


@lru_cache
def get_gemini_settings() -> GeminiSettings:
    return GeminiSettings()
