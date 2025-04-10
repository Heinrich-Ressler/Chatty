import httpx
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_session
from app.utils.audit import log_action

router = APIRouter(prefix="/admin/users", tags=["Admin Users"])

AUTH_SERVICE_URL = "http://auth:8000"  # это имя сервиса из docker-compose

def check_admin(x_role: str = Header(...)):
    if x_role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

async def get_users_from_auth_service():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{AUTH_SERVICE_URL}/users")
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to fetch users from Auth Service")
        return response.json()

@router.get("/", summary="Список пользователей")
async def list_users(x_role: str = Depends(check_admin)):
    return await get_users_from_auth_service()

@router.post("/{user_id}/block", summary="Заблокировать пользователя")
async def block_user(user_id: int, x_role: str = Depends(check_admin)):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{AUTH_SERVICE_URL}/users/{user_id}/block")
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to block user")
        return response.json()


@router.post("/{user_id}/unblock", summary="Разблокировать пользователя")
async def unblock_user(user_id: int, x_role: str = Depends(check_admin)):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{AUTH_SERVICE_URL}/users/{user_id}/unblock")
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to unblock user")
        return response.json()


@router.patch("/{user_id}/role", summary="Изменить роль пользователя")
async def change_role(user_id: int, new_role: str, x_role: str = Depends(check_admin)):
    async with httpx.AsyncClient() as client:
        response = await client.patch(
            f"{AUTH_SERVICE_URL}/users/{user_id}/role",
            json={"role": new_role}
        )
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to change user role")
        return response.json()


@router.post("/{user_id}/block", summary="Заблокировать пользователя")
async def block_user(
    user_id: int,
    x_role: str = Depends(check_admin),
    x_user_id: int = Header(...),
    session: AsyncSession = Depends(get_session)
):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{AUTH_SERVICE_URL}/users/{user_id}/block")
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to block user")

    await log_action(session, admin_id=x_user_id, action="block_user", target_id=user_id)

    return response.json()

