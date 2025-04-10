from fastapi import APIRouter, Depends, Header, HTTPException
import httpx
from app.routes.admin_users import check_admin

router = APIRouter(prefix="/admin", tags=["Admin Stats"])

AUTH_SERVICE_URL = "http://auth:8000"
POST_SERVICE_URL = "http://post:8000"

@router.get("/stats", summary="Общая статистика пользователей и постов")
async def get_stats(x_role: str = Depends(check_admin)):
    async with httpx.AsyncClient() as client:
        # Получаем статистику по пользователям
        users_resp = await client.get(f"{AUTH_SERVICE_URL}/users/stats")
        posts_resp = await client.get(f"{POST_SERVICE_URL}/stats")

        if users_resp.status_code != 200 or posts_resp.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to fetch stats from services")

        users_stats = users_resp.json()
        posts_stats = posts_resp.json()

        return {
            "users_total": users_stats["total"],
            "users_blocked": users_stats["blocked"],
            "users_active": users_stats["active"],
            "posts_total": posts_stats["posts"],
            "comments_total": posts_stats["comments"]
        }

