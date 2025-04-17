import redis.asyncio as redis
from app.core.config import settings
import json

redis_client = redis.from_url(settings.redis_url, decode_responses=True)

async def get_cached_feed(user_id: int) -> list[dict] | None:
    data = await redis_client.get(f"feed:{user_id}")
    if data:
        return json.loads(data)
    return None

async def set_cached_feed(user_id: int, posts: list[dict]):
    await redis_client.setex(
        f"feed:{user_id}",
        settings.feed_cache_expire,
        json.dumps(posts)
    )

async def invalidate_feeds_of_followers(user_ids: list[int]):
    if not user_ids:
        return
    await redis_client.delete(*[f"feed:{uid}" for uid in user_ids])
