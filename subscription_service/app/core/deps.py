from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.clients.clients import AuthClient

auth_scheme = HTTPBearer()
auth_client = AuthClient()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)
) -> int:
    token = credentials.credentials
    user_id = await auth_client.get_user_id_by_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user_id




