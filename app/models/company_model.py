from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID

from models.user_model import UserBaseModel
from schemas.company import CompanyMode


class SearchCompanyModel():
    def __init__(self, name, mode, owner_id, page, size) -> None:
        self.name = name
        self.mode = mode
        self.owner_id = owner_id
        self.page = page
        self.size = size

class CompanyModel(BaseModel):
    name: str
    description: Optional[str]
    mode: CompanyMode = Field(default=CompanyMode.ACTIVE)
    owner_id: Optional[UUID] = None
    
    class Config:
        json_schema_extra = {
            'example': {
                "name": "NashTech",
                "description": "Delivering technology excellence",
                "mode": "ACTIVE"
            }
        }

class CompanyViewModel(BaseModel):
    id: UUID
    name: str
    description: str | None = None
    mode: CompanyMode
    owner: UserBaseModel | None
    
    class Config:
        from_attributes: True
        
class CompanyUserModel(BaseModel):
    id: UUID
    name: str
    mode: CompanyMode

    class Config:
        from_attributes: True