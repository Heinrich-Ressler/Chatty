from fastapi import FastAPI
from app.routes import admin_users
from app.routes import admin_content
from app.routes import admin_logs
from app.routes import admin_stats
app = FastAPI(title="Admin Service")  # <-- сначала создаём FastAPI

app.include_router(admin_users.router)  # <-- потом подключаем роутер
app.include_router(admin_content.router)
app.include_router(admin_logs.router)
app.include_router(admin_stats.router)
@app.get("/")
def read_root():
    return {"message": "Admin Service is running"}



