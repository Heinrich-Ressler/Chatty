from pydantic_settings import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv
import os

load_dotenv(
    verbose=True,
    override=True,
    dotenv_path="C:/Users/Tel-ran.de/PycharmProjects/Chatty/.env"
)

class Settings(BaseSettings):

    # Основная БД
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    # Тестовая БД
    TEST_DB_HOST: str
    TEST_DB_PORT: str
    TEST_DB_NAME: str
    TEST_DB_USER: str
    TEST_DB_PASSWORD: str

    # Прочее
    DEBUG: bool = True

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def TEST_DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASSWORD}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"

    AUTH_SERVICE_URL: str = "http://auth:8000"
    POST_SERVICE_URL: str = "http://post:8000"
    SECRET_KEY: str = "super-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        from_attributes = True

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
