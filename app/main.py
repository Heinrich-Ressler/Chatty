from fastapi import FastAPI
from . import posts, auth


app = FastAPI()

app.include_router(posts.router)
app.include_router(auth.router, prefix="/auth", tags=["Registration"])


