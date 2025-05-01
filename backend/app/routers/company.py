from datetime import timedelta
from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import User
from ..schemas import Company, CompanyCreate, CompanyUpdate
from ..models.models import Company as CompanyModel, User as UserModel
from ..utils.auth import (
    get_current_active_user
)
from ..config import settings

router = APIRouter(
    prefix="/companies",
    tags=["companies"],
)

@router.get("/", response_model=List[Company])
async def get_companies(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_active_user)
    ):
    companies = db.query(CompanyModel).offset(skip).limit(limit).all()
    return companies


@router.get("/{company_id}", response_model=Company)
async def get_company(company_id: int, 
                      db: Session = Depends(get_db),
                      user: UserModel = Depends(get_current_active_user)
                      ):
    company = db.query(CompanyModel).filter(CompanyModel.id == company_id).first()
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@router.put("/{company_id}", response_model=Company)
async def update_company(company_id: int, 
                         company: CompanyUpdate, 
                         db: Session = Depends(get_db),
                         user: UserModel = Depends(get_current_active_user)
                         ):
    db_company = db.query(CompanyModel).filter(CompanyModel.id == company_id).first()
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")

    for key, value in company.dict(exclude_unset=True).items():
        setattr(db_company, key, value)

    db.commit()
    db.refresh(db_company)
    return db_company

@router.delete("/{company_id}")
async def delete_company(company_id: int, 
                         db: Session = Depends(get_db),
                         user: UserModel = Depends(get_current_active_user)):
    db_company = db.query(CompanyModel).filter(CompanyModel.id == company_id).first()
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")

    db.delete(db_company)
    db.commit()
    return {"message": "Company deleted successfully"}

@router.post("/create", response_model=Company)
async def create_company(company: CompanyCreate,
                         db: Session = Depends(get_db),
                         user: UserModel = Depends(get_current_active_user)):
    

    db_company = CompanyModel(
            name = company.name,
            industry = company.industry,
            region = company.region,
            short_about = company.short_about,
            long_about = company.long_about,
            brand_colors = company.brand_colors,
            brand_font = company.brand_font,
            logo_url = company.logo_url,
            brand_book_url = company.brand_book_url,
            user_id = user.id
    )

    db.add(db_company)
    db.commit()
    db.refresh(db_company)

    return db_company

@router.get("/me", response_model=User)
async def read_users_me(current_user: UserModel = Depends(get_current_active_user)):
    return current_user