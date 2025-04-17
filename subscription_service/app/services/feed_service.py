from app.services.subscription_service import get_following
from app.clients import PostClient
from app.utils.cache import get_cached_feed, set_cached_feed

post_client = PostClient()

async def get_user_feed(user_id: int) -> list[dict]:
    cached = await get_cached_feed(user_id)
    if cached:
        return cached

    following_ids = await get_following(user_id)
    if not following_ids:
        return []

    posts = await post_client.fetch_posts(following_ids)
    await set_cached_feed(user_id, posts)
    return posts
