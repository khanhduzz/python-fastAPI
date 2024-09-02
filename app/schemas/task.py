from database import Base
from sqlalchemy import Column, Enum, ForeignKey, SmallInteger, String, Uuid
from sqlalchemy.orm import relationship

from .base_entity import BaseEntity, TaskStatus


class Task(BaseEntity, Base):
    __tablename__ = "tasks"

    summary = Column(String)
    description = Column(String)
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.DRAFT)
    priority = Column(SmallInteger, nullable=False)
    staff_id = Column(Uuid, ForeignKey("users.id"))
    owner_id = Column(Uuid, ForeignKey("users.id"), nullable=False)

    # staff = relationship("User", back_populates="tasks", foreign_keys="Task.staff_id")
    # owner = relationship("User", back_populates="tasks_created", foreign_keys="Task.owner_id")
