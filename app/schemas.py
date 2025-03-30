from pydantic import BaseModel, EmailStr

# Схема регистрации
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    nickname: str

# Схема входа:
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Ответ пользователю (без пароля)
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    nickname: str

    class Config:
        orm_mode = True  # для совместимости с ORM

# Схема для создания поста
class PostCreate(BaseModel):
    title: str
    content: str

# Схема для ответа по посту
class Post(PostCreate):
    id: int
    user_id: int
    created_at: str

    class Config:
        orm_mode = True