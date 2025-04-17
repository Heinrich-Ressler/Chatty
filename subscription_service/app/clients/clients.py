import httpx
from fastapi import Request, HTTPException

from app.core.config import settings


class AuthClient:
    def __init__(self, base_url: str = settings.AUTH_SERVICE_URL):
        self.base_url = base_url

    async def get_current_user_id(self, request: Request) -> int:
        token = self._extract_token(request)
        return await self.get_user_id_by_token(token)

    async def get_user_id_by_token(self, token: str) -> int:
        headers = {"Authorization": f"Bearer {token}"}
        url = f"{self.base_url}/auth/internal/user-id"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()["user_id"]
        elif response.status_code == 401:
            raise HTTPException(status_code=401, detail="Unauthorized")
        else:
            raise HTTPException(status_code=500, detail="Auth service error")

    @staticmethod
    def _extract_token(request: Request) -> str:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=403, detail="Authorization token missing")
        return auth_header.split(" ")[1]


class PostClient:
    def __init__(self, base_url: str = settings.POST_SERVICE_URL):
        self.base_url = base_url

    async def fetch_posts(self, user_ids: list[int]) -> list[dict]:
        url = f"{self.base_url}/posts/internal"
        payload = {"user_ids": user_ids}

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)

        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=500, detail="Post service error")


# Удобный короткий доступ
auth_client = AuthClient()
post_client = PostClient()


