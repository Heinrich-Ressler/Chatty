from fastapi import APIRouter, Request, Depends, HTTPException
from typing import List
from app.clients.clients import AuthClient, PostClient
from app.schemas.schemas import Post
from app.services.subscription_service import get_following
from app.core.deps import get_current_user
from app.services.subscription_service import subscribe, unsubscribe, get_following
from app.utils.cache import get_cached_feed, set_cached_feed
from app.clients.clients import PostClient

router = APIRouter()

auth_client = AuthClient()
post_client = PostClient()

@router.get("/feed", response_model=List[Post])
async def feed(current_user: int = Depends(get_current_user)):
    cached = await get_cached_feed(current_user)
    if cached:
        return cached

    user_ids = await get_following(user_id=current_user)
    posts = await post_client.fetch_posts(user_ids)
    await set_cached_feed(current_user, posts)
    return posts

