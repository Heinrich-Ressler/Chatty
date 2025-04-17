from fastapi import FastAPI
from app.routes import admin_users
from app.routes import admin_content
from app.routes import admin_logs
from app.routes import admin_stats


from app.routes import (
    admin_users,
    admin_content,
    admin_logs,
    admin_stats,
)

app = FastAPI(
    title="Admin Service",
    description="Управление пользователями, модерация контента и аудит",
    version="1.0.0"
)

# Подключаем роутеры
app.include_router(admin_users.router)
app.include_router(admin_content.router)
app.include_router(admin_logs.router)
app.include_router(admin_stats.router)

@app.get("/")
def root():
    return {"message": "Admin Service is alive and ruling"}



