from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID

from schemas.company import CompanyMode


class SearchCompanyModel():
    def __init__(self, name, mode, page, size) -> None:
        self.name = name
        self.mode = mode
        self.page = page
        self.size = size

class CompanyModel(BaseModel):
    name: str
    description: Optional[str]
    mode: CompanyMode = Field(default=CompanyMode.ACTIVE)
    owner_id: UUID
    
    class Config:
        json_schema_extra = {
            'example': {
                "name": "NashTech",
                "description": "Delivering technology excellence",
                "mode": "ACTIVE",
                "owner_id": "123e4567-e89b-12d3-a456-426614174000",
            }
        }

class CompanyViewModel(BaseModel):
    id: UUID
    name: str
    description: str | None = None
    mode: CompanyMode
    owner_id: UUID
    
    class Config:
        from_attributes: True