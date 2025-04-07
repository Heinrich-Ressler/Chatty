from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.config import settings  # Избегаем относительного импорта
from app.models import Base  # Обращаемся к модели через абсолютный импорт
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные окружения из .env файла

DATABASE_URL = "sqlite:///./chatty.db"

# Создание синхронного и асинхронного движков базы данных
async_engine = create_async_engine(settings.DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


# Асинхронная сессия БД
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


# Функция инициализации базы данных
def init_db():
    Base.metadata.create_all(bind=engine)
