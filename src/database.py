import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    postgres_user: str = os.getenv("POSTGRES_USER", "gameuser")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "gamepass")
    postgres_db: str = os.getenv("POSTGRES_DB", "cockroachdb")
    postgres_host: str = os.getenv("POSTGRES_HOST", "db")
    postgres_port: str = os.getenv("POSTGRES_PORT", "5432")
    redis_url: str = os.getenv("REDIS_URL", "redis://redis:6379")
    telegram_token: str = os.getenv("TELEGRAM_TOKEN", "")

settings = Settings()

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.postgres_user}:{settings.postgres_password}@"
    f"{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, pool_size=20, max_overflow=30)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()