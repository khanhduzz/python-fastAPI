from uuid import UUID
from starlette import status
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user import User
from database import get_async_db_context, get_db_context
from models.staffModel import SearchStaffModel, StaffModel, StaffViewModel
from services.exception import AccessDeniedError, ResourceNotFoundError
from services import staffService as StaffService
from services import auth as AuthService

router = APIRouter(prefix="/staffs", tags=["Staffs"])

@router.get("", response_model=list[StaffViewModel])
async def get_all_staffs(
    full_name: str = Query(default=None),
    email: str = Query(default=None),
    company_id: UUID = Query(default=None),
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=50, default=10),
    async_db: AsyncSession = Depends(get_async_db_context),
    user: User = Depends(AuthService.token_interceptor),
    ):
        if not user.is_admin:
            raise AccessDeniedError()
        conds = SearchStaffModel(full_name, email, company_id, page, size)
        return await StaffService.get_staffs(async_db)


@router.get("/{staff_id}", status_code=status.HTTP_200_OK, response_model=StaffViewModel)
async def get_staff_by_id(staff_id: UUID, db: Session = Depends(get_db_context)):    
    staff = StaffService.get_staff_by_id(db, staff_id)

    if staff is None:
        raise ResourceNotFoundError()

    return staff


@router.post("", status_code=status.HTTP_201_CREATED, response_model=StaffViewModel)
async def create_staff(
    request: StaffModel, 
    db: Session = Depends(get_db_context),
    user: User = Depends(AuthService.token_interceptor)
    ):
        if not user.is_admin:
            raise AccessDeniedError()
        return StaffService.add_new_staff(db, request)


@router.put("/{staff_id}", status_code=status.HTTP_200_OK, response_model=StaffViewModel)
async def update_staff(
    staff_id: UUID,
    request: StaffModel,
    db: Session = Depends(get_db_context),
    user: User = Depends(AuthService.token_interceptor)
    ):
        if not user.is_admin:
            raise AccessDeniedError()
        return StaffService.update_staff(db, staff_id, request)


@router.delete("/{staff_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_staff(
    staff_id: UUID, 
    db: Session = Depends(get_db_context),
    user: User = Depends(AuthService.token_interceptor)
    ):
        if not user.is_admin:
            raise AccessDeniedError()
        StaffService.delete_staff(db, staff_id)
