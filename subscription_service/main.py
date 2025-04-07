from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.feed import router as feed_router
from routers.subscription import router as subscription_router
from faststream.rabbit.fastapi import RabbitRouter, Logger

router = RabbitRouter("amqp://guest:guest@rabbitmq:5672/")
app = FastAPI(
    title="Subscription Service",
    version="1.0.0"
)

app = FastAPI(
    title="Subscription API",
    version="1.0.0",
    openapi_url="/openapi.json",  # внутренний путь, без префикса
    docs_url="/docs",  # внутренний путь, без префикса
    redoc_url="/redoc",
    root_path="/api",  # внешний префикс
    root_path_in_servers=True  # включаем генерацию серверов с префиксом
)


@app.get("/send")
async def hello_http():
    await router.broker.publish("Hello, Rabbit!", queue="test")
    return "Message sent"

# Подключаем роутеры
app.include_router(subscription_router, prefix="/subscriptions", tags=["Subscriptions"])
app.include_router(feed_router, prefix="/feed", tags=["Feed"])

@app.get("/")
def read_root():
    return {"message": "Subscription Service is running"}