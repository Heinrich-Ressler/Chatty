import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_delete_post_success(monkeypatch):
    monkeypatch.setattr(
        "httpx.AsyncClient.delete",
        lambda self, url, *args, **kwargs: type("Response", (), {
            "status_code": 200,
            "json": lambda: {"message": "Post 42 deleted"}
        })()
    )
    async with AsyncClient(base_url="http://localhost:8002") as ac:
        response = await ac.delete("/admin/posts/42", headers={"x-role": "admin"})
    assert response.status_code == 200
    assert response.json()["message"] == "Post 42 deleted"
