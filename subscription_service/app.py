from utils.cache import invalidate_feeds_of_followers
from subscription_service.app import get_followers_ids

async def handle_post_created(user_id: int):
    follower_ids = await get_followers_ids(user_id)
    await invalidate_feeds_of_followers(follower_ids)

def callback(ch, method, properties, body):
    event = json.loads(body)
    print(f"Received event: {event}")

    if event['event'] == "PostCreated":
        asyncio.run(handle_post_created(event['user_id']))

