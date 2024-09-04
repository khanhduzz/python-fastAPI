from datetime import datetime
from typing import Optional
from uuid import UUID

from models.user_model import UserBaseModel
from pydantic import BaseModel, Field
from schemas.task import TaskStatus


class SearchTaskModel:
    def __init__(self, summary, staff_id, owner_id, page, size) -> None:
        self.summary = summary
        self.staff_id = staff_id
        self.owner_id = owner_id
        self.page = page
        self.size = size


class TaskModel(BaseModel):
    summary: str
    description: Optional[str]
    status: TaskStatus = Field(default=TaskStatus.DRAFT)
    priority: int = Field(default=1)
    staff_id: Optional[UUID] = None
    owner_id: UUID

    class Config:
        json_schema_extra = {
            "example": {
                "summary": "Create Python project with FastAPI",
                "description": "Use Python with FastAPI to create a website about staffs and tasks management",
                "status": "DRAFT",
                "priority": 1,
                "staff_id": "123e4567-e89b-12d3-a456-426614174000",
                "owner_id": "123e4567-e89b-12d3-a456-426614174000",
            }
        }


class TaskViewModel(BaseModel):
    id: UUID
    summary: str
    description: str | None = None
    status: TaskStatus
    priority: int
    staff_id: UUID | None = None
    owner_id: UUID
    staff: UserBaseModel | None
    owner: UserBaseModel | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
