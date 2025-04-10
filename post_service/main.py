from fastapi import FastAPI
from database import Base, engine
from routers import posts  # импортируем роуты
from sqlalchemy import create_engine
from config import settings
app = FastAPI()


# используем sync engine только для миграций или create_all
sync_engine = create_engine(settings.sync_database_url)

# подключаем роуты
app.include_router(posts.router)

@app.get("/")
def root():
    return {"message": "Post service работает!"}

