import asyncpg
from config import DATABASE_URL
from typing import Annotated, cast
from fastapi import Depends
from collections.abc import AsyncGenerator


_pool: asyncpg.Pool | None = None


async def get_pool() -> asyncpg.Pool:
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(DATABASE_URL)
    return _pool


async def close_pool() -> None:
    global _pool
    if _pool:
        await _pool.close()
        _pool = None


async def get_db() -> AsyncGenerator[asyncpg.Connection[asyncpg.Record]]:
    pool = await get_pool()
    async with pool.acquire() as conn:
        # PoolConnectionProxy は Connection のサブクラスであり、インターフェースは同一。
        # asyncpg-stubs が型レベルで区別するため cast で型チェッカーに伝える。
        yield cast(asyncpg.Connection[asyncpg.Record], conn)


DB = Annotated[asyncpg.Connection, Depends(get_db)]
