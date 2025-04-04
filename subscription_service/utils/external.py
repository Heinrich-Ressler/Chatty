import httpx
from fastapi import HTTPException

from app.config import settings


async def fetch_user_by_token(token: str) -> dict:
    """
    Получение текущего пользователя через Auth-сервис.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.AUTH_SERVICE_URL}/auth/me",
                headers={"Authorization": f"Bearer {token}"}
            )
        response.raise_for_status()
    except httpx.HTTPError:
        raise HTTPException(status_code=401, detail="Authentication failed")

    return response.json()


async def fetch_posts_for_users(user_ids: list[int]) -> list[dict]:
    """
    Получение ленты постов по списку user_ids из Post-сервиса.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.POST_SERVICE_URL}/posts/feed",
                json={"user_ids": user_ids}
            )
        response.raise_for_status()
    except httpx.HTTPError:
        raise HTTPException(status_code=502, detail="Post service unavailable")

    return response.json()