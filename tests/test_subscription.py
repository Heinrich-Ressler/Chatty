import pytest
from httpx import AsyncClient
from fastapi import status
from app.main import app


@pytest.mark.asyncio
async def test_subscribe_flow():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Эмулируем заголовок авторизации (в идеале — мок токена)
        headers = {"Authorization": "Bearer test-token"}

        # Мокаем get_current_user через зависимость (можно monkeypatch'ом или override_dependency)
        app.dependency_overrides = {
            # Импортируй actual deps.get_current_user
            # и замени на lambda: {"id": 1}
        }

        # Подписка
        response = await ac.post("/subscriptions/subscribe/2", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["detail"] == "Subscribed to user 2"

        # Получение подписок
        response = await ac.get("/subscriptions/subscriptions", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        assert 2 in response.json()["subscriptions"]

        # Отписка
        response = await ac.delete("/subscriptions/unsubscribe/2", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["detail"] == "Unsubscribed from user 2"

        # Проверяем, что отписались
        response = await ac.get("/subscriptions/subscriptions", headers=headers)
        assert 2 not in response.json()["subscriptions"]