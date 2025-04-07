from pydantic import BaseModel
from datetime import datetime


class SubscriptionCreate(BaseModel):
    user_id: int
    follower_id: int


class SubscriptionOut(BaseModel):
    id: int


class Post(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    created_at: datetime


class UserOut(BaseModel):
    id: int
    email: str
