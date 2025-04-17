from fastapi import FastAPI
from faststream.rabbit.fastapi import RabbitRouter
from app.broker.consumer import broker
from app.routers import feed
from fastapi import FastAPI
from app.routers import feed, subscription
from app.broker.consumer import broker
from faststream.rabbit.fastapi import RabbitRouter, Logger


router = RabbitRouter("amqp://guest:guest@rabbitmq:5672/")

@router.subscriber("test")
@router.publisher("response")
async def hello(message, logger: Logger):
    logger.info(message)
    return "Hello, response!"


@router.subscriber("test")
async def get_message(message, logger: Logger):
    logger.info(message)


app = FastAPI(
    title="Subscription API",
    version="1.0.0",
    openapi_url="/openapi.json",  # внутренний путь, без префикса
    docs_url="/docs",  # внутренний путь, без префикса
    redoc_url="/redoc",
    root_path="/api",  # внешний префикс
    root_path_in_servers=True  # включаем генерацию серверов с префиксом
)

# Подключаем роутеры
app.include_router(feed.router, prefix="/feed", tags=["Feed"])
app.include_router(subscription.router, prefix="/subscriptions", tags=["Subscriptions"])
app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Subscription Service is running"}

@app.get("/send")
async def send_message():
   await router.broker.publish("Hello, Rabbit!", queue="test")
   return "Message sent"


@router.subscriber("test")
async def get_message(message, logger):
   logger.info(message)

if __name__ == "__main__":
    import asyncio
    asyncio.run(broker.start())