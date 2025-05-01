from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import datetime

from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())

    company = relationship("Company", back_populates="owner", uselist=False)
    social_accounts = relationship("SocialMediaAccount", back_populates="user")
    posts = relationship("Post", back_populates="user")

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    industry = Column(String)
    region = Column(String)
    short_about = Column(String, nullable=True)
    long_about = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    brand_colors = Column(String, nullable=True)
    brand_font = Column(String, nullable=True)
    logo_url = Column(String, nullable=True)
    brand_book_url = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="company")
    #social_accounts = relationship("SocialMediaAccount", back_populates="company")

#

class SocialMediaAccount(Base):
    __tablename__ = "social_media_accounts"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String)  # instagram, tiktok, telegram, whatsapp - потом вынесем в отдельный справочник
    account_id = Column(String)
    access_token = Column(String, nullable=True)
    refresh_token = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="social_accounts")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)  # story, feed, reels - потом вынесем в обдельную таблицу
    content = Column(Text)
    hashtags = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
    is_published = Column(Boolean, default=False)
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="posts")

