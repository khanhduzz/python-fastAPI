from typing import List
from uuid import UUID

from models.user_model import SearchUserModel, UserModel
from schemas.user import User, get_password_hash
from services import utils
from services.exception import ResourceNotFoundError
from sqlalchemy import select
from sqlalchemy.orm import Session


def get_users(db: Session, conds: SearchUserModel) -> List[User]:
    query = select(User)

    if conds.company_id is not None:
        query = query.filter(User.company_id == conds.company_id)
    if conds.email is not None:
        query = query.filter(User.email.ilike(f"%{conds.email}%"))
    if conds.full_name is not None:
        query = query.filter(User.full_name.ilike(f"%{conds.full_name}%"))
        
    query = query.offset((conds.page-1)*conds.size).limit(conds.size)
    
    return db.scalars(query).all()

def get_user_by_id(db: Session, user_id: UUID) -> User:
    return db.scalars(select(User).filter(User.id == user_id)).first()


def add_new_user(db: Session, data: UserModel) -> User:
    user = User(**data.model_dump())

    user.created_at = utils.get_current_utc_time()
    user.updated_at = utils.get_current_utc_time()
    user.password = get_password_hash(data.password)

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
