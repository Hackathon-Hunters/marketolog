from pydantic import BaseModel
from typing import Optional

class CompanyBase(BaseModel):
    name: str
    industry: str
    region: str
    short_about: str
    long_about: Optional[str] = None
    brand_colors: Optional[str] = None
    brand_font: Optional[str] = None
    logo_url: Optional[str] = None
    brand_book_url: Optional[str] = None

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(CompanyBase):
    name: Optional[str] = None
    industry: Optional[str] = None
    region: Optional[str] = None
    sort_about: Optional[str] = None
    long_about: Optional[str] = None
    brand_colors: Optional[str] = None
    brand_font: Optional[str] = None
    logo_url: Optional[str] = None
    brand_book_url: Optional[str] = None

class Company(CompanyBase):
    pass