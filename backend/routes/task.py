from uuid import uuid4, UUID
from fastapi import APIRouter, HTTPException, status

from database import DB
from repositories import task_repository
from schemas.task import TaskCreate, TaskListResponse, TaskResponse, TaskUpdate

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("", response_model=TaskListResponse)
async def get_tasks(db: DB):
    records = await task_repository.get_tasks(db)
    return {"tasks": records}


@router.post("", response_model=TaskResponse)
async def create_task(body: TaskCreate, db: DB):
    record = await task_repository.create_task(db, uuid4(), body.title, "in_progress")
    return record


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: UUID, task_data: TaskUpdate, db: DB):
    update_data = task_data.model_dump(exclude_unset=True)
    record = await task_repository.update_task(db, task_id=task_id, **update_data)

    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return record
