from uuid import UUID

from models.user_model import UserModel
from schemas import User
from services import utils
from services.exception import ResourceNotFoundError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session


async def get_users(async_db: AsyncSession) -> list[User]:
    result = await async_db.scalars(select(User).order_by(User.created_at))

    return result.all()


def get_user_by_id(db: Session, user_id: UUID) -> User:
    return db.scalars(select(User).filter(User.id == user_id)).first()


def add_new_user(db: Session, data: UserModel) -> User:
    user = User(**data.model_dump())

    user.created_at = utils.get_current_utc_time()
    user.updated_at = utils.get_current_utc_time()

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def update_user(db: Session, id: UUID, data: UserModel) -> User:
    user = get_user_by_id(db, id)

    if user is None:
        raise ResourceNotFoundError()

    user.username = data.username
    user.first_name = data.first_name
    user.last_name = data.last_name
    user.full_name = data.full_name
    user.updated_at = utils.get_current_utc_time()

    db.commit()
    db.refresh(user)

    return user


def delete_user(db: Session, id: UUID) -> None:
    user = get_user_by_id(db, id)

    if user is None:
        raise ResourceNotFoundError()

    db.delete(user)
    db.commit()
