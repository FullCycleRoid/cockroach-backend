import os
from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(Enum):
    PROD = "PROD"
    DEV = "DEV"
    LOCAL = "LOCAL"

    @property
    def is_local(self) -> bool:
        if self == "LOCAL":
            return True
        return False

    @property
    def is_prod(self) -> bool:
        if self == "PROD":
            return True
        return False

    @property
    def is_dev(self) -> bool:
        if self == "DEV":
            return True
        return False


class Settings(BaseSettings):
    ENVIRONMENT: Environment

    POSTGRES_USER: str = "gameuser"
    POSTGRES_PASSWORD: str = "gamepass"
    POSTGRES_DB: str = "cockroachdb"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    REDIS_URL: str = "redis://redis:6379"
    TELEGRAM_TOKEN: str = ""
    DEBUG_MODE: str = ""

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )


settings = Settings()
