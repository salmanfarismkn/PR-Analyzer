from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "PR Sentinel"
    debug: bool = True

    api_v1_prefix: str = "/api/v1"

    secret_key: str

    database_url: str

    redis_url: str

    github_client_id: str = ""
    github_client_secret: str = ""
    github_webhook_secret: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()