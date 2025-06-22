import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Получаем настройки из переменных окружения
POSTGRES_USER = os.getenv("POSTGRES_USER", "gameuser")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "gamepass")
POSTGRES_DB = os.getenv("POSTGRES_DB", "cockroachdb")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "db")  # Используем 'db' по умолчанию
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")

# Формируем строку подключения
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# Выводим для отладки (убрать в продакшене)
print(f"Connecting to database: {SQLALCHEMY_DATABASE_URL}")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=30
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
