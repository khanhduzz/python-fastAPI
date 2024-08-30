import enum

from database import Base
from sqlalchemy import Column, ForeignKey, String, Uuid
from sqlalchemy.orm import relationship

from .base_entity import BaseEntity, CompanyMode


class Company(BaseEntity, Base):
    __tablename__ = "Companies"

    name = Column(String)
    description = Column(String)
    mode = Column(enum.Enum(CompanyMode), nullable=False, default=CompanyMode.ACTIVE)
    owner_id = Column(Uuid, ForeignKey("users.id"), nullable=False)

    staffs = relationship("User", back_populates="employees")
    owner = relationship("User", back_populates="owner")
