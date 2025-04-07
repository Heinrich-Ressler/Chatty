import pytest
import httpx

BASE_URL = "http://localhost:8007"  #subscription_service
AUTH_URL = "http://localhost:8003"  #auth_service
POST_URL = "http://localhost:8006"  #post_service

@pytest.mark.asyncio
async def test_full_subscription_flow():
    async with httpx.AsyncClient() as client:
        # 1. Register User A
        res = await client.post(f"{AUTH_URL}/auth/register", json={
            "email": "usera@example.com",
            "password": "password"
        })
        assert res.status_code == 200

        # 2. Login User A
        res = await client.post(f"{AUTH_URL}/auth/token", data={
            "username": "usera@example.com",
            "password": "password"
        })
        token_a = res.json()["access_token"]
        headers_a = {"Authorization": f"Bearer {token_a}"}

        # 3. Create Post as User A
        res = await client.post(f"{POST_URL}/posts/", json={
            "title": "Hello",
            "content": "From User A"
        }, headers=headers_a)
        assert res.status_code == 200

        # 4. Register User B
        res = await client.post(f"{AUTH_URL}/auth/register", json={
            "email": "userb@example.com",
            "password": "password"
        })
        assert res.status_code == 200

        # 5. Login User B
        res = await client.post(f"{AUTH_URL}/auth/token", data={
            "username": "userb@example.com",
            "password": "password"
        })
        token_b = res.json()["access_token"]
        headers_b = {"Authorization": f"Bearer {token_b}"}

        # 6. Subscribe User B to User A
        res = await client.post(f"{BASE_URL}/subscriptions/subscribe/1", headers=headers_b)
        assert res.status_code == 200

        # 7. User B retrieves feed and sees post from User A
        res = await client.get(f"{BASE_URL}/feed", headers=headers_b)
        assert res.status_code == 200
        posts = res.json()
        assert any(p["title"] == "Hello" and p["content"] == "From User A" for p in posts)
