from fastapi import FastAPI
from app import posts


app = FastAPI()

app.include_router(posts.router)
