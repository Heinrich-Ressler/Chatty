from faststream.rabbit import RabbitBroker
from pydantic import BaseModel
from app.utils.cache import invalidate_feeds_of_followers
from app.services.subscription_service import get_followers_ids

broker = RabbitBroker("amqp://guest:guest@rabbitmq")

class PostCreatedEvent(BaseModel):
    event: str
    user_id: int

@broker.subscriber("events")
async def handle_post_created(msg: PostCreatedEvent):
    if msg.event == "PostCreated":
        followers = await get_followers_ids(msg.user_id)
        await invalidate_feeds_of_followers(followers)


