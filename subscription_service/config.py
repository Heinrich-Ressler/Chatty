from pydantic_settings import BaseSettings, SettingsConfigDict

class SubscriptionSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env.local', extra='ignore', case_sensitive=False
    )

    db_host: str = 'subscription_db'
    db_port: int = 5432
    db_name: str = 'SubscriptionDB'
    db_user: str = 'postgres'
    db_password: str = 'postgres'

    @property
    def async_database_url(self) -> str:
        return f'postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}'

settings = SubscriptionSettings()









