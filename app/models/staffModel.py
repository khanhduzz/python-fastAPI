from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID

class SearchStaffModel():
    def __init__(self, full_name, email, company_id, page, size) -> None:
        self.full_name = full_name
        self.email = email
        self.company_id = company_id
        self.page = page
        self.size = size

class StaffModel(BaseModel):
    full_name: str = Field(min_length=2)

class StaffViewModel(BaseModel):
    id: UUID 
    full_name: str
    created_at: datetime | None = None
    
    class Config:
        from_attributes = True
