from typing import List
from sqlalchemy import UUID, select
from sqlalchemy.orm import Session, joinedload

from services.exception import InvalidInputError, ResourceNotFoundError
from schemas.company import Company
from models.company_model import CompanyModel, SearchCompanyModel
from services import user_service as UserService

def get_companies(db: Session, conds: SearchCompanyModel) -> List[Company]:
    if conds.name is not None:
        query = query.filter(Company.name.like(f"{conds.name}%"))
    if conds.mode is not None:
        query = query.filter(Company.mode.value == conds.mode.value)
        
    query.offset((conds.page - 1) * conds.size).limit(conds.size)
    
    return db.scalars(query).all()

def get_company_by_id(db: Session, id: UUID, /, joined_load=False) -> Company:
    query = select(Company).filter(Company.id == id)
    
    if joined_load:
        query.options(joinedload(Company.owner, innerjoin=True))
        
    return db.scalars(query).first()

def add_new_country(db: Session, data: CompanyModel) -> Company:
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
    
    db.commit()
    db.refresh(company)
    
    return company