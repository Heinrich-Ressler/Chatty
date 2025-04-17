from sqlalchemy.ext.asyncio import AsyncSession
from app.db import AuditLog

async def log_action(session: AsyncSession, admin_id: int, action: str, target_id: int):
    log_entry = AuditLog(
        admin_id=admin_id,
        action=action,
        target_id=target_id,
    )
    session.add(log_entry)
    await session.commit()
