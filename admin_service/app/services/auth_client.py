import httpx

AUTH_SERVICE_URL = "http://auth_service:8003"

async def get_all_users():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{AUTH_SERVICE_URL}/users")
        response.raise_for_status()
        return response.json()
