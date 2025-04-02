from fastapi import FastAPI
from post import posts
from auth import auth

app = FastAPI()

app.include_router(posts.router)
app.include_router(auth.router, prefix="/auth", tags=["Registration"])


