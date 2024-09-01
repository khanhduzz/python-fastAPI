from datetime import datetime
from enum import Enum
import uuid

from sqlalchemy import Column, DateTime, Uuid, event


class Gender(Enum):
    NONE = "N"
    FEMALE = "F"
    MALE = "M"


class CompanyMode(Enum):
    ACTIVE = "A"
    INACTIVE = "I"
    SUSPENDED = "S"


class TaskStatus(Enum):
    DRAFT = "D"
    OPEN = "O"
    PROCESSING = "P"
    CLOSED = "P"
    CANCELED = "C"


class UserRole(Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"


class BaseEntity:
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
