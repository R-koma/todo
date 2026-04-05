from uuid import uuid4
from fastapi import APIRouter

from database import DB
from repositories import task_repository
from schemas.task import TaskCreate, TaskListResponse, TaskResponse

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("", response_model=TaskListResponse)
async def get_tasks(db: DB):
    records = await task_repository.get_tasks(db)
    return {"tasks": records}


@router.post("", response_model=TaskResponse)
async def create_task(body: TaskCreate, db: DB):
    record = await task_repository.create_task(db, uuid4(), body.title, "in_progress")
    return record
