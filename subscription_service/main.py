from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from subscription_service import routers
app = FastAPI(
    title="Subscription Service",
    version="1.0.0"
)

# CORS — если фронт отдельно
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # или ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(routers.subscription, prefix="/subscriptions", tags=["Subscriptions"])
app.include_router(routers.feed, prefix="/feed", tags=["Feed"])

# Можно добавить root
@app.get("/")
def root():
    return {"msg": "Subscription Service is running!"}