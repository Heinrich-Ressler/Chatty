from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db import AuditLog, get_session
from app.routes.admin_users import check_admin

router = APIRouter(prefix="/admin", tags=["Audit Logs"])

@router.get("/logs", summary="Просмотр логов действий админов")
async def get_logs(session: AsyncSession = Depends(get_session), x_role: str = Depends(check_admin)):
    result = await session.execute(select(AuditLog).order_by(AuditLog.timestamp.desc()))
    return [dict(row._mapping) for row in result]
