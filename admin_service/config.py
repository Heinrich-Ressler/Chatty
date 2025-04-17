from pydantic_settings import BaseSettings, SettingsConfigDict
from auth_service import crud, config


class AdminSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Database
    DB_HOST: str = "admin_db"
    DB_PORT: int = 5432
    DB_NAME: str = "AdminDB"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"

    # External services
    POST_SERVICE_URL: str = "http://post_service:8006"
    AUTH_SERVICE_URL: str = "http://auth_service:8003"
    SUBSCRIPTION_SERVICE_URL: str = "http://subscription_service:8007"

    # RabbitMQ
    RABBITMQ_HOST: str = "rabbitmq"
    RABBITMQ_PORT: int = 5672

    @property
    def database_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = AdminSettings()
