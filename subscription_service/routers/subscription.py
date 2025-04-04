from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, delete, select

from subscription_service import deps, schemas
from subscription_service.models import Subscription

router = APIRouter()

@router.post("/subscribe/{user_id}")
async def subscribe(
    user_id: int,
    db: AsyncSession = Depends(deps.get_db_session),
    current_user=Depends(deps.get_current_user)
):
    if user_id == current_user["id"]:
        raise HTTPException(status_code=400, detail="Cannot subscribe to yourself")

    stmt = insert(Subscription).values(user_id=user_id, follower_id=current_user["id"]).prefix_with("OR IGNORE")
    await db.execute(stmt)
    await db.commit()
    return {"detail": f"Subscribed to user {user_id}"}


@router.delete("/unsubscribe/{user_id}")
async def unsubscribe(
    user_id: int,
    db: AsyncSession = Depends(deps.get_db_session),
    current_user=Depends(deps.get_current_user)
):
    stmt = delete(Subscription).where(
        Subscription.user_id == user_id,
        Subscription.follower_id == current_user["id"]
    )
    await db.execute(stmt)
    await db.commit()
    return {"detail": f"Unsubscribed from user {user_id}"}


@router.get("/subscriptions")
async def get_subscriptions(
    db: AsyncSession = Depends(deps.get_db_session),
    current_user=Depends(deps.get_current_user)
):
    stmt = select(Subscription.user_id).where(Subscription.follower_id == current_user["id"])
    result = await db.execute(stmt)
    ids = [row[0] for row in result.fetchall()]
    return {"subscriptions": ids}


@router.get("/followers")
async def get_followers(
    db: AsyncSession = Depends(deps.get_db_session),
    current_user=Depends(deps.get_current_user)
):
    stmt = select(Subscription.follower_id).where(Subscription.user_id == current_user["id"])
    result = await db.execute(stmt)
    ids = [row[0] for row in result.fetchall()]
    return {"followers": ids}