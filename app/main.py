from dotenv import load_dotenv
from fastapi import FastAPI
from app import posts, auth  # Абсолютный импорт вместо относительного
from fastapi.security import OAuth2PasswordBearer
from app.config import settings  # Убедитесь, что объект settings правильно настроен

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token",
    scopes={}  # 👈 это говорит Swagger: \"не использовать client_id и client_secret\"
)
app = FastAPI(debug=settings.DEBUG)

# Указываем правильный путь к токену — /auth/token
app.include_router(posts.router)
app.include_router(auth.router, prefix="/auth", tags=["Registration"])
