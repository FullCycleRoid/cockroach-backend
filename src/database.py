from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    postgres_user: str = "gameuser"
    postgres_password: str = "gamepass"
    postgres_db: str = "cockroachdb"
    postgres_host: str = "db"
    postgres_port: str = "5432"
    redis_url: str = "redis://redis:6379"

    class Config:
        env_file = ".env"

settings = Settings()

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.postgres_user}:{settings.postgres_password}@"
    f"{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()