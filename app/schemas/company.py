
from database import Base
from sqlalchemy import Column, ForeignKey, String, Uuid, Enum
from sqlalchemy.orm import relationship

from .base_entity import BaseEntity, CompanyMode


class Company(BaseEntity, Base):
    __tablename__ = "companies"

    name = Column(String)
    description = Column(String)
    mode = Column(Enum(CompanyMode), nullable=False, default=CompanyMode.ACTIVE)
    owner_id = Column(Uuid, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="companies_created", foreign_keys=[owner_id])
    staffs = relationship("User", back_populates="company", foreign_keys="User.company_id")