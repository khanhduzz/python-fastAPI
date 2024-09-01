from pydantic import BaseModel, Field
from sqlalchemy import UUID

from schemas.company import CompanyMode


class SearchCompanyModel():
    def __init__(self, name, mode, page, size) -> None:
        self.name = name
        self.mode = mode
        self.page = page
        self.size = size

class CompanyModel(BaseModel):
    name: str
    description: str
    mode = CompanyMode = Field(default = CompanyMode.ACTIVE)
    owner_id = UUID
    
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
    mode = CompanyMode | CompanyMode.ACTIVE = CompanyMode.ACTIVE