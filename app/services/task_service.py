from typing import List
from uuid import UUID

from models.task_model import SearchTaskModel, TaskModel
from schemas.task import Task
from services import user_service as UserService
from services.exception import InvalidInputError, ResourceNotFoundError
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload


def get_tasks(db: Session, conds: SearchTaskModel) -> List[Task]:
    query = select(Task)
    
    if conds.summary is not None:
        query = query.filter(Task.summary.ilike(f"%{conds.summary}%"))
    if conds.staff_id is not None:
        query = query.filter(Task.staff_id == conds.staff_id)
    if conds.owner_id is not None:
        query = query.filter(Task.owner_id == conds.owner_id)

    query = query.offset((conds.page - 1) * conds.size).limit(conds.size)

    return db.scalars(query).all()


def get_task_by_id(db: Session, id: UUID, /, joined_load=False) -> Task:
    query = select(Task).filter(Task.id == id)

    if joined_load:
        query.options(joinedload(Task.owner, innerjoin=True))

    return db.scalars(query).first()


def add_new_task(db: Session, data: TaskModel) -> Task:
    owner = UserService.get_user_by_id(db, data.owner_id)

    if owner is None:
        raise InvalidInputError("Invalid owner information")

    task = Task(**data.model_dump())

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def update_task(db: Session, id: UUID, data: TaskModel) -> Task:
    task = get_task_by_id(db, id)

    if task is None:
        raise ResourceNotFoundError()

    if data.owner_id is not None and data.owner_id != task.owner_id:
        owner = UserService.get_user_by_id(db, data.owner_id)
        if owner is None:
            raise InvalidInputError("Invalid owner information")

    task.summary = data.summary
    task.description = data.description
    task.status = data.status
    task.priority = data.priority
    task.staff_id = data.staff_id

    db.commit()
    db.refresh(task)

    return task

def delete_task(db: Session, id: UUID) -> None:
    task = get_task_by_id(db, id)

    if task is None:
        raise ResourceNotFoundError()

    db.delete(task)
    db.commit()