import os
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from dotenv import load_dotenv
from main import app
from database import get_db
import asyncpg


load_dotenv(".env.test", override=True)

TEST_DATABASE_URL = os.getenv("DATABASE_URL")


@pytest_asyncio.fixture(scope="session")
async def test_pool():
    pool = await asyncpg.create_pool(TEST_DATABASE_URL)
    yield pool
    await pool.close()


@pytest_asyncio.fixture(autouse=True)
async def clean_db(test_pool):
    yield
    async with test_pool.acquire() as conn:
        await conn.execute("TRUNCATE TABLE tasks CASCADE")


@pytest_asyncio.fixture
async def client(test_pool):
    """
    Provide an httpx.AsyncClient configured to call the ASGI `app` while overriding the app's `get_db` dependency to yield a connection from the supplied test_pool.
    
    Parameters:
        test_pool: An asyncpg connection pool used to acquire a connection for each request.
    
    Returns:
        ac: An AsyncClient instance bound to the ASGI app and base URL "http://test". The fixture yields the client; after use the dependency override is cleared.
    """
    async def override_get_db():
        async with test_pool.acquire() as conn:
            yield conn

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def sample_task(client):
    response = await client.post("/api/tasks", json={"title": "Buy milk"})
    return response.json()
