from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from schemas.base_entity import UserRole


class UserModel(BaseModel):
    username: str
    email: Optional[str]
    full_name: str
    first_name: str
    last_name: str


class UserBaseModel(BaseModel):
    id: UUID
    username: str
    email: str | None = None
    first_name: str
    last_name: str

    class Config:
        from_attributes = True


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
