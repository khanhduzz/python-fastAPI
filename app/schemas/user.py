from database import Base
from passlib.context import CryptContext
from schemas.base_entity import BaseEntity
from sqlalchemy import Boolean, Column, ForeignKey, String, Uuid
from sqlalchemy.orm import relationship

bcrypt_context = CryptContext(schemes=["bcrypt"])


class User(BaseEntity, Base):
    __tablename__ = "users"

    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    company_id = Column(Uuid, ForeignKey("company.id"))

    tasks = relationship("Task", back_populates="staff")
    tasks_created = relationship("Task", back_populates="owner")


def get_password_hash(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hased_password):
    return bcrypt_context.verify(plain_password, hased_password)
