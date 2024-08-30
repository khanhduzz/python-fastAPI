from typing import List
from uuid import UUID

from database import get_db_context
from fastapi import APIRouter, Depends, Query, status
from models.task_model import SearchTaskModel, TaskModel, TaskViewModel
from schemas import user as User
from services import auth as AuthService
from services import task_service as TaskService
from services.exception import *
from sqlalchemy.orm import Session

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# This is a mock data for testing
# TASKS = [{"id": i, "summary": f"Task summary {i}", "description": f"Description {i%3 + 1}"}, "status": "{i%2 ? OPEN : CLOSED}", "priority": {i} for i in range(1, 11)]


@router.get("", status_code=status.HTTP_200_OK, response_model=List[TaskViewModel])
async def get_all_tasks(
    summary: str = Query(default=None),
    staff_id: UUID = Query(default=None),
    owner_id: UUID = Query(default=None),
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=50, default=10),
    db: Session = Depends(get_db_context),
    user: User = Depends(AuthService.token_interceptor),
):
    if not user.is_admin:
        raise AccessDeniedError()

    conds = SearchTaskModel(summary, staff_id, owner_id, page, size)
    return TaskService.get_tasks(db, conds)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=TaskViewModel)
async def create_task(
    request: TaskModel,
    user: User = Depends(AuthService.token_interceptor),
    db: Session = Depends(get_db_context),
):
    if not user:
        raise AccessDeniedError()

    request.owner_id = user.id

    return TaskService.add_new_task(db, request)


@router.get("/{task_id}", response_model=TaskViewModel)
async def get_task_detail(task_id: UUID, db: Session = Depends(get_db_context)):
    task = TaskService.get_task_by_id(db, task_id, joined_load=True)

    if task is None:
        raise ResourceNotFoundError()

    return task


@router.put("/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskViewModel)
async def update_task(
    task_id: UUID,
    request: TaskModel,
    db: Session = Depends(get_db_context),
    user: User = Depends(AuthService.token_interceptor),
):
    task = TaskService.get_task_by_id(db, task_id, joined_load=True)
    if task is None:
        raise ResourceNotFoundError()
    if not ((user and task.owner != user) or user.is_admin):
        raise AccessDeniedError()
    return TaskService.update_task(db, task_id, request)
