import enum
from sqlalchemy import Column, ForeignKey, SmallInteger, String, Uuid, Enum
from sqlalchemy.orm import relationship
from database import Base
from .base_entity import BaseEntity, TaskStatus

class Task(BaseEntity, Base):
    __tablename__ = "tasks"

    summary = Column(String)
    description = Column(String)
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.DRAFT)
    priority = Column(SmallInteger, nullable=False)
    staff_id = Column(Uuid, ForeignKey("users.id"))
    owner_id = Column(Uuid, ForeignKey("users.id"), nullable=False)

    staff = relationship("User", back_populate="tasks")
    owner = relationship("User", back_populate="tasks_created")
