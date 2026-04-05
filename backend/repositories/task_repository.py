from uuid import UUID
import asyncpg


async def get_tasks(conn: asyncpg.Connection):
    query = """--sql
      SELECT id, title, status, created_at, updated_at
      FROM tasks
    """

    records = await conn.fetch(query)
    return [dict(r) for r in records]


async def create_task(conn: asyncpg.Connection, task_id: UUID, title: str, status: str):
    query = """--sql
      INSERT INTO tasks (id, title, status)
      VALUES ($1, $2, $3)
      RETURNING id, title, status, created_at, updated_at
    """
    record = await conn.fetchrow(query, task_id, title, status)
    return dict(record)
