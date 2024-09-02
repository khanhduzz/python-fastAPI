
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

    staffs = relationship("User", back_populates="company")
    owner = relationship("User", back_populates="companies")
