from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TaskResponse(BaseModel):
    id: UUID
    title: str
    status: str
    created_at: datetime
    updated_at: datetime


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str | None = None
    status: str | None = None

class TaskListResponse(BaseModel):
    tasks: list[TaskResponse]
