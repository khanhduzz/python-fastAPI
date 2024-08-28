from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.staff import Staff
from services import utils
from models.staffModel import StaffModel
from schemas import Staff
from services.exception import ResourceNotFoundError


async def get_staffs(async_db: AsyncSession) -> list[Staff]:
    result = await async_db.scalars(select(Staff).order_by(Staff.created_at))
    
    return result.all()

def get_staff_by_id(db: Session, staff_id: UUID) -> Staff:
    return db.scalars(select(Staff).filter(Staff.id == staff_id)).first()

def add_new_staff(db: Session, data: StaffModel) -> Staff:
    staff = Staff(**data.model_dump())

    staff.created_at = utils.get_current_utc_time()
    staff.updated_at = utils.get_current_utc_time()
    
    db.add(staff)
    db.commit()
    db.refresh(staff)
    
    return staff

def update_staff(db: Session, id: UUID, data: StaffModel) -> Staff:
    staff = get_staff_by_id(db, id)

    if staff is None:
        raise ResourceNotFoundError()
    
    staff.full_name = data.full_name
    staff.updated_at = utils.get_current_utc_time()
    
    db.commit()
    db.refresh(staff)

    return staff

def delete_staff(db: Session, id: UUID) -> None:
    staff = get_staff_by_id(db, id)

    if staff is None:
        raise ResourceNotFoundError()
    
    db.delete(staff)
    db.commit()
