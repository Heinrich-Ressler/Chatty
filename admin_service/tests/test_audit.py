import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.audit import log_action
from app.db import AuditLog
import pytest
from sqlalchemy import select

@pytest.mark.asyncio
async def test_block_user_logs(monkeypatch):
    called = {}

    async def mock_log(session, admin_id, action, target_id):
        called.update({"admin_id": admin_id, "action": action, "target_id": target_id})

    monkeypatch.setattr("app.routes.admin_users.log_action", mock_log)
    monkeypatch.setattr("httpx.AsyncClient.post", lambda *a, **kw: type("Resp", (), {"status_code": 200, "json": lambda: {"message": "OK"}})())

    async with AsyncClient(base_url="http://localhost:8002") as ac:
        await ac.post("/admin/users/123/block", headers={"x-role": "admin", "x-user-id": "42"})

    assert called == {"admin_id": 42, "action": "block_user", "target_id": 123}

@pytest.mark.asyncio
async def test_log_action_adds_entry(async_session: AsyncSession):
    # Arrange: входные данные
    admin_id = 1
    action = "delete_post"
    target_id = 123

    # Act: вызываем логирование
    await log_action(async_session, admin_id, action, target_id)

    # Assert: запись действительно появилась
    result = await async_session.execute(
        select(AuditLog).where(AuditLog.admin_id == admin_id, AuditLog.action == action)
    )
    entry = result.scalars().first()
    assert entry is not None
    assert entry.target_id == target_id

@pytest.mark.asyncio
async def test_log_action_writes_to_db(async_session):
    # Arrange
    admin_id = 99
    action = "delete_comment"
    target_id = 456

    # Act
    await log_action(async_session, admin_id, action, target_id)

    # Assert
    result = await async_session.execute(
        select(AuditLog).where(
            AuditLog.admin_id == admin_id,
            AuditLog.action == action,
            AuditLog.target_id == target_id
        )
    )
    entry = result.scalar_one_or_none()
    assert entry is not None
    assert entry.action == action
