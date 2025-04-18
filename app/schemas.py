
from typing import List, Any
from fastapi import Form
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv

load_dotenv()  # По умолчанию ищет .env в корне проекта


class SubscriptionCreate(BaseModel):
    user_id: int

    class Config:
        from_attributes = True


class Post(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    created_at: str

    class Config:
        from_attributes = True



# Схема для создания поста

class PostCreate(BaseModel):
    title: str
    content: str

    class Config:
        from_attributes = True





# Схема регистрации

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    nickname: str

    class Config:
        from_attributes = True



# Схема входа:

class UserLogin(BaseModel):
    email: str

    class Config:
        from_attributes = True



    class Config:
        from_attributes = True


# Ответ пользователю (без пароля)
class UserResponse(BaseModel):

    id: int
    email: EmailStr

    class Config:

        from_attributes = True

class UserRead(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True




class EmailPasswordForm:
    def __init__(
        self,
        email: str = Form(...),
        password: str = Form(...)
    ):
        self.username = email  # чтобы не ломался код, который ожидает .username
        self.password = password




class TokenData(BaseModel):
    email: str | None = None

