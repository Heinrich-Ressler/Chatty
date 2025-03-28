from fastapi import FastAPI
from . import posts


app = FastAPI()

app.include_router(posts.router)


