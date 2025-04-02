#from fastapi import FastAPI
#from . import posts, auth
#from fastapi import FastAPI, Depends
#from fastapi.security import OAuth2PasswordBearer

#app = FastAPI()

#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")  # 👈 вот эта строка активирует окно авторизации в Swagger

#app.include_router(posts.router)
#app.include_router(auth.router, prefix="/auth", tags=["Registration"])

from fastapi import FastAPI
from . import posts, auth
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token",
    scopes={}  # 👈 это говорит Swagger: \"не использовать client_id и client_secret\"
)
app = FastAPI()

#Указываем правильный путь к токену — /auth/token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

app.include_router(posts.router)
app.include_router(auth.router, prefix="/auth", tags=["Registration"])


