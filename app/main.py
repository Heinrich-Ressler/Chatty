#from fastapi import FastAPI
#from . import posts, auth
#from fastapi import FastAPI, Depends
#from fastapi.security import OAuth2PasswordBearer

#app = FastAPI()

#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")  # 👈 вот эта строка активирует окно авторизации в Swagger

#app.include_router(posts.router)
#app.include_router(auth.router, prefix="/auth", tags=["Registration"])

from fastapi import FastAPI

from . import posts, auth, models
from app.database import init_db
from .utils.security import oauth2_scheme


app = FastAPI(
    title="Chatty API",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    root_path="",
    root_path_in_servers=True
)

#Указываем правильный путь к токену — /auth/token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

app.include_router(posts.router)
app.include_router(auth.router, prefix="/auth", tags=["Registration"])


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def read_root():
    return {"message": "Welcome to Chatty API"}


