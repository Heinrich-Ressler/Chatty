from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    author_id: int

class PostUpdate(PostBase):
    pass

class PostOut(PostBase):
    id: int
    author_id: int
    created_at: datetime
    image_url: Optional[str] = None

    class Config:
        orm_mode = True


class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    post_id: int
    author_id: int

class CommentUpdate(CommentBase):
    pass

class CommentOut(CommentBase):
    id: int
    post_id: int
    author_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class LikeOut(BaseModel):
    id: int
    post_id: int
    user_id: int

    class Config:
        orm_mode = True
