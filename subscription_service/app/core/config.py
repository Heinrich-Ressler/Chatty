from pydantic_settings import BaseSettings, SettingsConfigDict


class SubscriptionSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env.local',
        extra='ignore',
        case_sensitive=False,
    )

    # === DB ===
    db_host: str = 'subscription_db'
    db_port: int = 5432
    db_name: str = 'SubscriptionDB'
    db_user: str = 'postgres'
    db_password: str = 'postgres'

    # === External Services ===
    AUTH_SERVICE_URL: str = "http://auth_service:8003"
    POST_SERVICE_URL: str = "http://post_service:8006"
    ADMIN_SERVICE_URL: str = "http://admin_service:8009"

    # === Redis ===
    redis_host: str = 'redis'
    redis_port: int = 6379
    feed_cache_expire: int = 60  # seconds

    # RabbitMQ
    RABBITMQ_HOST: str = "rabbitmq"
    RABBITMQ_PORT: int = 5672

    # === Computed properties ===
    @property
    def async_database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}"


settings = SubscriptionSettings()











