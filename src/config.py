from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str =  "gameuser"
    POSTGRES_PASSWORD: str = "gamepass"
    POSTGRES_DB: str = "cockroachdb"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: str = "5432"
    REDIS_URL: str = "redis://redis:6379"
    TELEGRAM_TOKEN: str = ""

settings = Settings()