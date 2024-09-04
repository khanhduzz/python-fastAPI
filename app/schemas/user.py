
from database import Base
from passlib.context import CryptContext
from sqlalchemy import Boolean, Column, ForeignKey, String, Uuid, Enum
from sqlalchemy.orm import relationship

from .base_entity import BaseEntity, UserRole

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
    role = Column(Enum(UserRole), nullable=False, default=UserRole.USER)
    company_id = Column(Uuid, ForeignKey("companies.id"))

    tasks = relationship("Task", back_populates="staff", foreign_keys="Task.staff_id")
    tasks_created = relationship("Task", back_populates="owner" , foreign_keys="Task.owner_id")
    companies_created = relationship("Company", back_populates="owner", foreign_keys="Company.owner_id")
    company = relationship("Company", back_populates="staffs", foreign_keys="User.company_id")

def get_password_hash(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hased_password):
    return bcrypt_context.verify(plain_password, hased_password)
