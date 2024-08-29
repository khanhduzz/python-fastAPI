import datetime
import enum
import uuid

from sqlalchemy import Column, DateTime, Uuid, event


class Gender(enum.Enum):
    NONE = "N"
    FEMALE = "F"
    MALE = "M"


class CompanyMode(enum.Enum):
    ACTIVE = "A"
    INACTIVE = "I"
    SUSPENDED = "S"


class TaskStatus(enum.Enum):
    DRAFT = "D"
    OPEN = "O"
    PROCESSING = "P"
    CLOSED = "P"
    CANCELED = "C"


class UserRole(enum.Enum):
    USER = "U"
    ADMIN = "A"
    SUPER_ADMIN = "S"


class BaseEntity:
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    created_by = Column(Uuid, nullable=False)


# Event listeners to set created_at and updated_at
@event.listens_for(BaseEntity, "before_insert")
def set_created_at(mapper, connection, target):
    target.created_at = datetime.now()
    target.updated_at = datetime.now()


@event.listens_for(BaseEntity, "before_update")
def set_updated_at(mapper, connection, target):
    target.updated_at = datetime.now()
