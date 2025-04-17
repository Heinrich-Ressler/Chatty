from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from app.models.models import Subscription
from app.core.db import SessionLocal

async def subscribe(follower_id: int, user_id: int):
    async with SessionLocal() as session:
        sub = Subscription(user_id=user_id, follower_id=follower_id)
        session.add(sub)
        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()
            raise

async def unsubscribe(follower_id: int, user_id: int):
    async with SessionLocal() as session:
        await session.execute(
            delete(Subscription).where(
                Subscription.user_id == user_id,
                Subscription.follower_id == follower_id
            )
        )
        await session.commit()

async def get_following(user_id: int):
    async with SessionLocal() as session:
        result = await session.execute(
            select(Subscription.user_id).where(Subscription.follower_id == user_id)
        )
        return [row[0] for row in result.all()]

async def get_followers_ids(user_id: int) -> list[int]:
    async with SessionLocal() as session:
        result = await session.execute(
            select(Subscription.follower_id).where(Subscription.user_id == user_id)
        )
        return [row[0] for row in result.fetchall()]

