from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class TaskResponse(BaseModel):
    id: UUID
    title: str
    status: str
    created_at: datetime
    updated_at: datetime


class TaskCreate(BaseModel):
    title: str = Field(min_length=1)


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1)
    status: str | None = None


class TaskListResponse(BaseModel):
    tasks: list[TaskResponse]
