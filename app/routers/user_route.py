from typing import List
from uuid import UUID

from database import get_async_db_context, get_db_context
from fastapi import APIRouter, Depends, Query
from models.user_model import SearchUserModel, UserBaseModel, UserModel, UserViewModel
from schemas.base_entity import UserRole
from schemas.user import User
from services import auth as AuthService
from services import user_service as UserService
from services.exception import AccessDeniedError, ResourceNotFoundError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette import status

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", status_code=status.HTTP_200_OK, response_model=List[UserBaseModel])
async def get_user(db: Session = Depends(get_db_context)) -> List[UserViewModel]:
    # return db.scalars(select(User).filter_by(role = "ADMIN")).all()
    return db.query(User).filter(User.role == "ADMIN").all()


@router.get("", status_code=status.HTTP_200_OK, response_model=list[UserViewModel])
async def get_users(
    full_name: str = Query(default=None),
    email: str = Query(default=None),
    company_id: UUID = Query(default=None),
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=50, default=10),
    async_db: AsyncSession = Depends(get_async_db_context),
    user: User = Depends(AuthService.token_interceptor),
):
    if user.role != "ADMIN":
        raise AccessDeniedError()
    
    conds = SearchUserModel(full_name, email, company_id, page, size)
    return await UserService.get_users(async_db, conds)


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserViewModel)
async def get_user_detail(user_id: UUID, db: Session = Depends(get_db_context)):
    staff = UserService.get_user_by_id(db, user_id)

    if staff is None:
        raise ResourceNotFoundError()

    return staff


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserViewModel)
async def create_user(
    request: UserModel,
    db: Session = Depends(get_db_context),
    user: User = Depends(AuthService.token_interceptor),
):
    if user.role != "ADMIN":
        raise AccessDeniedError()
    return UserService.add_new_user(db, request)


@router.put("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserViewModel)
async def update_user(
    user_id: UUID,
    request: UserModel,
    db: Session = Depends(get_db_context),
    user: User = Depends(AuthService.token_interceptor),
):
    if user.role != "ADMIN":
        raise AccessDeniedError()
    return UserService.update_user(db, user_id, request)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_one_user(
    user_id: UUID,
    db: Session = Depends(get_db_context),
    user: User = Depends(AuthService.token_interceptor),
):
    if user.role != "ADMIN":
        raise AccessDeniedError()
    UserService.delete_user(db, user_id)
