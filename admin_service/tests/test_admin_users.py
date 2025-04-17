import pytest
from httpx import AsyncClient

# Тест на получение списка пользователей (если роль admin)
@pytest.mark.asyncio
async def test_get_users_list_success():
    async with AsyncClient(base_url="http://localhost:8002") as ac:
        response = await ac.get("/admin/users/", headers={"x-role": "admin"})

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# Тест на блокировку пользователя (если роль admin)
@pytest.mark.asyncio
async def test_block_user_success():
    async with AsyncClient(base_url="http://localhost:8002") as ac:
        response = await ac.post("/admin/users/1/block", headers={"x-role": "admin"})

    assert response.status_code == 200
    assert "message" in response.json()


# Тест на разблокировку пользователя (мок Auth Service)
@pytest.mark.asyncio
async def test_unblock_user_success(monkeypatch):
    monkeypatch.setattr(
        "httpx.AsyncClient.post",
        lambda self, url, *args, **kwargs: type("Response", (), {
            "status_code": 200,
            "json": lambda: {"message": "User 1 unblocked"}
        })()
    )

    async with AsyncClient(base_url="http://localhost:8002") as ac:
        response = await ac.post("/admin/users/1/unblock", headers={"x-role": "admin"})

    assert response.status_code == 200
    assert response.json() == {"message": "User 1 unblocked"}


# Тест на смену роли пользователя (мок Auth Service)
@pytest.mark.asyncio
async def test_change_user_role_success(monkeypatch):
    monkeypatch.setattr(
        "httpx.AsyncClient.patch",
        lambda self, url, *args, **kwargs: type("Response", (), {
            "status_code": 200,
            "json": lambda: {"message": "User 1 role changed to moderator"}
        })()
    )

    async with AsyncClient(base_url="http://localhost:8002") as ac:
        response = await ac.patch(
            "/admin/users/1/role?new_role=moderator",
            headers={"x-role": "admin"}
        )

    assert response.status_code == 200
    assert response.json() == {"message": "User 1 role changed to moderator"}


# Тест на блокировку с неадминской ролью (ожидается 403)
@pytest.mark.asyncio
async def test_block_user_forbidden_for_non_admin():
    async with AsyncClient(base_url="http://localhost:8002") as ac:
        response = await ac.post("/admin/users/1/block", headers={"x-role": "user"})

    assert response.status_code == 403
    assert response.json()["detail"] == "Access denied"

