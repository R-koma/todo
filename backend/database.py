import asyncpg
from config import DATABASE_URL
from typing import Annotated
from fastapi import Depends


_pool: asyncpg.Pool | None = None


async def get_pool() -> asyncpg.Pool:
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(DATABASE_URL)
    return _pool


async def close_pool():
    global _pool
    if _pool:
        await _pool.close()
        _pool = None


async def get_db() -> asyncpg.Connection:
    pool = await get_pool()
    async with pool.acquire() as conn:
        yield conn


DB = Annotated[asyncpg.Connection, Depends(get_db)]
