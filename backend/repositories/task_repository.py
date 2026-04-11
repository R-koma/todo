from uuid import UUID
import asyncpg


async def get_tasks(conn: asyncpg.Connection) -> dict | None:
    query = """--sql
      SELECT id, title, status, created_at, updated_at
      FROM tasks
    """

    records = await conn.fetch(query)
    return [dict(r) for r in records]


async def create_task(conn: asyncpg.Connection, task_id: UUID, title: str, status: str) -> dict | None:
    query = """--sql
      INSERT INTO tasks (id, title, status)
      VALUES ($1, $2, $3)
      RETURNING id, title, status, created_at, updated_at
    """
    record = await conn.fetchrow(query, task_id, title, status)
    return dict(record)


async def update_task(conn: asyncpg.Connection, task_id: UUID, title: str | None = None, status: str | None = None):
    query = """--sql
      UPDATE tasks
      SET title = COALESCE($2, title),
          status = COALESCE($3, status),
          updated_at = NOW()
      WHERE id = $1
      RETURNING id, title, status, created_at, updated_at
    """

    record = await conn.fetchrow(query, task_id, title, status)
    return dict(record) if record else None


async def delete_task(conn: asyncpg.Connection, task_id: UUID) -> bool:
    query = """--sql
        DELETE FROM tasks
        WHERE id = $1
        RETURNING id
    """
    record = await conn.fetchrow(query, task_id)
    return record is not None
