from fastapi import APIRouter, Depends, HTTPException
from app.core.deps import get_current_user
from app.services.subscription_service import subscribe, unsubscribe, get_following
from typing import List
from app.schemas.schemas import Post
from app.utils.cache import get_cached_feed, set_cached_feed
from app.clients.clients import PostClient

router = APIRouter()
post_client = PostClient()

@router.post("/subscribe/{user_id}")
async def subscribe_user(user_id: int, current_user: int = Depends(get_current_user)):
    if user_id == current_user:
        raise HTTPException(status_code=400, detail="Can't subscribe to yourself")
    try:
        await subscribe(follower_id=current_user, user_id=user_id)
    except:
        raise HTTPException(status_code=409, detail="Already subscribed")
    return {"message": "Subscribed"}

@router.delete("/unsubscribe/{user_id}")
async def unsubscribe_user(user_id: int, current_user: int = Depends(get_current_user)):
    await unsubscribe(follower_id=current_user, user_id=user_id)
    return {"message": "Unsubscribed"}

@router.get("/subscriptions/following")
async def following(current_user: int = Depends(get_current_user)):
    return await get_following(user_id=current_user)




