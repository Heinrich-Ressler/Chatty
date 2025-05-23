from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db_base import Base  # Импортируем Base из db_base.py
from dotenv import load_dotenv


load_dotenv()  # По умолчанию ищет .env в корне проекта

# Модель пользователя
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    nickname = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False, default="user")

    # Связь: один пользователь — много постов
    posts = relationship("Post", back_populates="author")


# Модель поста
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Связь с автором поста
    author = relationship("User", back_populates="posts")