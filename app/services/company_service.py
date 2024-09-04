from typing import List
from uuid import UUID

from models.company_model import CompanyModel, SearchCompanyModel
from schemas.company import Company
from services import user_service as UserService
from services.exception import InvalidInputError, ResourceNotFoundError
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload


def get_companies(db: Session, conds: SearchCompanyModel) -> List[Company]:

    query = select(Company)

    if conds.name is not None:
        query = query.filter(Company.name.ilike(f"%{conds.name}%"))
    if conds.mode is not None:
        query = query.filter(Company.mode.value == conds.mode.value)
    if conds.owner_id is not None:
        query = query.filter(Company.owner_id == conds.owner_id)

    query = query.offset((conds.page - 1) * conds.size).limit(conds.size)

    return db.scalars(query).all()


def get_company_by_id(db: Session, id: UUID, /, joined_load=False) -> Company:
    query = select(Company).filter(Company.id == id)

    if joined_load:
        query.options(joinedload(Company.owner, innerjoin=True))

    return db.scalars(query).first()


def add_new_company(db: Session, data: CompanyModel) -> Company:
    owner = UserService.get_user_by_id(db, data.owner_id)

    if owner is None:
        raise InvalidInputError("Invalid owner information")

    company = Company(**data.model_dump())

    db.add(company)
    db.commit()
    db.refresh(company)

    return company


def update_company(db: Session, id: UUID, data: CompanyModel) -> Company:
    company = get_company_by_id(db, id)

    if company is None:
        raise ResourceNotFoundError()

    if data.owner_id != company.owner_id:
        owner = UserService.get_user_by_id(db, data.owner_id)
        if owner is None:
            raise InvalidInputError("Invalid owner information")

    company.name = data.name
    company.mode = data.mode
    company.description = data.description

    db.commit()
    db.refresh(company)

    return company


def delete_company(db: Session, id: UUID) -> None:
    company = get_company_by_id(db, id)

    if company is None:
        raise ResourceNotFoundError()

    db.delete(company)
    db.commit()
