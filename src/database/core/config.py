from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    USER: str
    PASSWORD: str
    DB: str
    HOST: str
    PORT: str

    model_config = SettingsConfigDict(
        env_prefix='POSTGRES_',
        env_file="./.env",
        extra='ignore'
    )


@lru_cache
def get_database_settings() -> DatabaseSettings:
    return DatabaseSettings()

def get_db_url() -> str:
    conf = get_database_settings()
    return f"postgresql+asyncpg://{conf.USER}:{conf.PASSWORD}@{conf.HOST}:{conf.PORT}/{conf.DB}"