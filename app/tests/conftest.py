import pytest_asyncio
from sqlalchemy import text
from app.db import async_session_maker


@pytest_asyncio.fixture
async def clear_users_after_test():
    yield
    async with async_session_maker() as session:
        await session.execute(text("DELETE FROM users"))
        await session.commit()
