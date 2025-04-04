from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from subscription_service import schemas, deps
from subscription_service.models import Subscription
from subscription_service.utils.external import fetch_posts_for_users

router = APIRouter()

@router.get("/feed", response_model=List[schemas.Post])
async def get_feed(
    db: AsyncSession = Depends(deps.get_db_session),
    current_user: dict = Depends(deps.get_current_user)
):
    # Получаем ID пользователей, на которых подписан текущий юзер
    result = await db.execute(
        select(Subscription.user_id).where(Subscription.follower_id == current_user["id"])
    )
    following_ids = [row[0] for row in result.fetchall()]

    if not following_ids:
        return []

    # Получаем посты через utils
    return await fetch_posts_for_users(following_ids)