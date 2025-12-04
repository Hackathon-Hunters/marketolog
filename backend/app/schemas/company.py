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
    telegram_bot_token: Optional[str] = None
    telegram_chat_id: Optional[str] = None

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    industry: Optional[str] = None
    region: Optional[str] = None
    short_about: Optional[str] = None
    long_about: Optional[str] = None
    brand_colors: Optional[str] = None
    brand_font: Optional[str] = None
    logo_url: Optional[str] = None
    brand_book_url: Optional[str] = None
    telegram_bot_token: Optional[str] = None
    telegram_chat_id: Optional[str] = None

class Company(CompanyBase):
    id: int
    
    class Config:
        from_attributes = True

class TelegramSettings(BaseModel):
    telegram_bot_token: Optional[str] = None
    telegram_chat_id: Optional[str] = None