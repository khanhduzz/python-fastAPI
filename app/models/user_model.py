from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from schemas.base_entity import UserRole


class UserModel(BaseModel):
    username: str
    email: Optional[str]
    password: str
    full_name: str
    first_name: str
    last_name: str
    company_id: Optional[UUID] | None
    role: str | None
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "david_malan",
                "email": "david@havard.com",
                "password": "password",
                "full_name": "David Malan",
                "first_name": "David",
                "last_name": "Malan",
                "company_id": "123e4567-e89b-12d3-a456-426614174000",
                "role": "USER",
            }
        }


class UserBaseModel(BaseModel):
    id: UUID
    username: str
    email: str | None = None
    first_name: str
    last_name: str
    company_id: Optional[UUID]

    class Config:
        from_attributes = True

class UserTaskModel(BaseModel):
    id: UUID
    username: str

class UserViewModel(UserBaseModel):
    role: UserRole
    created_at: datetime | None = None
    updated_at: datetime | None = None


class SearchUserModel:
    def __init__(self, full_name, email, company_id, page, size) -> None:
        self.full_name = full_name
        self.email = email
        self.company_id = company_id
        self.page = page
        self.size = size
