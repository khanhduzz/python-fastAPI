from datetime import datetime
from enum import Enum
import uuid

from sqlalchemy import Column, DateTime, Uuid, event


class Gender(Enum):
    NONE = "NONE"
    FEMALE = "FEMALE"
    MALE = "MALE"


class CompanyMode(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"


class TaskStatus(Enum):
    DRAFT = "DRAFT"
    OPEN = "OPEN"
    PROCESSING = "PROCESSING"
    CLOSED = "CLOSED"
    CANCELED = "CANCELED"


class UserRole(Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"


class BaseEntity:
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
