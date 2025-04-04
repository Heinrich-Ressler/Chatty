from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):

    DATABASE_URL: str = "postgresql+asyncpg://postgres:Tabasalu7@localhost:5432/chatty_db"

    AUTH_SERVICE_URL: str = "http://auth:8000"
    POST_SERVICE_URL: str = "http://post:8000"
    SECRET_KEY: str = "super-secret-key"  # для токенов
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()