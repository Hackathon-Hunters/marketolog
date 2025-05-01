from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from .company import Company

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    company: Optional[Company] = None

    class Config:
        from_attributes = True 