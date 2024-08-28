from typing import List
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from services import staffService as StaffService
from schemas import Task
from models.taskModel import TaskModel, SearchTaskModel
from services.utils import get_current_utc_time
from services.exception import ResourceNotFoundError, InvalidInputError


def get_tasks(db: Session, conds: SearchTaskModel) -> List[Task]:
    # Default of joinedload is LEFT OUTER JOIN
    query = select(Task).options(
        joinedload(Task.staff),
        joinedload(Task.owner, innerjoin=True))
    
    if conds.summary is not None:
        query = query.filter(Task.summary.like(f"{conds.summary}%"))
    if conds.staff_id is not None:
        query = query.filter(Task.staff_id == conds.staff_id)
    if conds.owner_id is not None:
        query = query.filter(Task.owner_id == conds.owner_id)
    
    query.offset((conds.page-1)*conds.size).limit(conds.size)
    
    return db.scalars(query).all()


def get_task_by_id(db: Session, id: UUID, /, joined_load = False) -> Task:
    query = select(Task).filter(Task.id == id)
    
    if joined_load:
        query.options(joinedload(Task.owner, innerjoin=True))
    
    return db.scalars(query).first()
    

def add_new_task(db: Session, data: TaskModel) -> Task:
    owner = StaffService.get_author_by_id(db, data.author_id)
        
    if owner is None:
        raise InvalidInputError("Invalid owner information")

    task = Task(**data.model_dump())
    task.created_at = get_current_utc_time()
    task.updated_at = get_current_utc_time()

    db.add(task)
    db.commit()
    db.refresh(task)
    
    return task

def update_task(db: Session, id: UUID, data: TaskModel) -> Task:
    task = get_task_by_id(db, id)

    if task is None:
        raise ResourceNotFoundError()

    if data.author_id != task.author_id:
        owner = StaffService.get_author_by_id(db, data.author_id)
        if owner is None:
            raise InvalidInputError("Invalid owner information")
    
    task.summary = data.summary
    task.description = data.description
    task.status = data.status
    task.priority = data.priority
    task.updated_at = get_current_utc_time()
    
    db.commit()
    db.refresh(task)
    
    return task
