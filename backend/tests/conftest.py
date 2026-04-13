import os
from typing import Any, AsyncGenerator, cast
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from dotenv import load_dotenv
from main import app
from database import get_db
import asyncpg


load_dotenv(".env.test", override=True)

TEST_DATABASE_URL = os.getenv("DATABASE_URL")


@pytest_asyncio.fixture(scope="session")
async def test_pool() -> AsyncGenerator[asyncpg.Pool, None]:
    pool = await asyncpg.create_pool(TEST_DATABASE_URL)
    yield pool
    await pool.close()


@pytest_asyncio.fixture(autouse=True)
async def clean_db(test_pool: asyncpg.Pool) -> AsyncGenerator[None, None]:
    yield
    async with test_pool.acquire() as conn:
        await conn.execute("TRUNCATE TABLE tasks CASCADE")


@pytest_asyncio.fixture
async def client(test_pool: asyncpg.Pool) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db() -> AsyncGenerator[asyncpg.Connection[asyncpg.Record], None]:
        async with test_pool.acquire() as conn:
            # PoolConnectionProxy は Connection のサブクラスであり、インターフェースは同一。
            # asyncpg-stubs が型レベルで区別するため cast で型チェッカーに伝える。
            yield cast(asyncpg.Connection[asyncpg.Record], conn)

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def sample_task(client: AsyncClient) -> dict[str, Any]:
    response = await client.post("/api/tasks", json={"title": "Buy milk"})
    return response.json()  # type: ignore[no-any-return]
