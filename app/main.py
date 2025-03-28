from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# Создаем экземпляр FastAPI приложения
app = FastAPI(
    title="Chatty",  # Название API
    description="Платформа для общения учеников и преподавателей",  # Описание
    version="0.1.0",  # Версия API
)





@app.get("/", tags=["root"])
async def root():
    return {
        "message": "Добро пожаловать в Chatty API!",

    }