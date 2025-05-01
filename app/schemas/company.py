from pydantic import BaseModel
from typing import Optional

class CompanyBase(BaseModel):
    name: str
    industry: str
    region: str
    brand_colors: Optional[str] = None
    brand_font: Optional[str] = None
    logo_url: Optional[str] = None
    brand_book_url: Optional[str] = None

class CompanyCreate(CompanyBase):
    pass

class Company(CompanyBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True 