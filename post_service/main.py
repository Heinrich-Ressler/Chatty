from fastapi import FastAPI
from .database import Base, engine
from .routers import posts  # ⬅️ импортируем роуты

app = FastAPI()

# создаём таблицы
Base.metadata.create_all(bind=engine)

# подключаем роуты
app.include_router(posts.router)

@app.get("/")
def root():
    return {"message": "Post service работает!"}

