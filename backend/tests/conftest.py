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
    app.dependency_overrides[get_db] = lambda: test_pool
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def sample_task(client):
    response = await client.post("/api/tasks", json={"title": "Buy milk"})
    return response.json()
