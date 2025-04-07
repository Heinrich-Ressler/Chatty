import httpx
from fastapi import HTTPException, Request
from config import settings

async def get_current_user_id(request: Request) -> int:
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{settings.AUTH_SERVICE_URL}/validate", headers={"Authorization": token})
        if resp.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid token")
        return resp.json()["user_id"]

async def fetch_posts(user_ids: list[int]) -> list[dict]:
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{settings.POST_SERVICE_URL}/posts/by_users",
            json={"user_ids": user_ids}
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=502, detail="Failed to fetch posts")
        return resp.json()
