import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_USER: str = "gameuser"
    POSTGRES_PASSWORD: str = "gamepass"
    POSTGRES_DB: str = "cockroachdb"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: str = "5432"
    REDIS_URL: str = "redis://redis:6379"
    TELEGRAM_TOKEN: str = ""

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )


settings = Settings()
