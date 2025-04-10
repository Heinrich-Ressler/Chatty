import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_admin_stats_success(monkeypatch):
    async def mock_get(url, *args, **kwargs):
        if "auth" in url:
            return type("Resp", (), {"status_code": 200, "json": lambda: {
                "total": 1000, "blocked": 50, "active": 950
            }})()
        if "post" in url:
            return type("Resp", (), {"status_code": 200, "json": lambda: {
                "posts": 1234, "comments": 5678
            }})()

    monkeypatch.setattr("httpx.AsyncClient.get", mock_get)

    async with AsyncClient(base_url="http://localhost:8002") as ac:
        response = await ac.get("/admin/stats", headers={"x-role": "admin"})

    assert response.status_code == 200
    assert response.json()["users_blocked"] == 50
    assert response.json()["posts_total"] == 1234
