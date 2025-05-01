from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from ..utils.auth import get_current_active_user
from ..models.models import User as UserModel, Post as PostModel
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)

class PostCreate(BaseModel):
    company_name: str
    business_type: str
    region: str
    language: str
    title: str
    description: str
    benefits: List[str]
    hashtags: List[str]
    image_prompt: str
    image_base64: Optional[str]

class PostResponse(BaseModel):
    id: int
    title: str
    description: str
    benefits: List[str]
    hashtags: List[str]
    image_base64: Optional[str]
    created_at: datetime
    is_published: bool

    class Config:
        from_attributes = True

@router.post("/", response_model=PostResponse)
async def create_post(
    post: PostCreate,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Создание нового поста"""
    try:
        db_post = PostModel(
            user_id=current_user.id,
            company_name=post.company_name,
            business_type=post.business_type,
            region=post.region,
            language=post.language,
            title=post.title,
            description=post.description,
            benefits=post.benefits,
            hashtags=post.hashtags,
            image_prompt=post.image_prompt,
            image_base64=post.image_base64
        )
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[PostResponse])
async def get_user_posts(
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Получение всех постов пользователя"""
    posts = db.query(PostModel).filter(PostModel.user_id == current_user.id).all()
    return posts

@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Получение конкретного поста"""
    post = db.query(PostModel).filter(
        PostModel.id == post_id,
        PostModel.user_id == current_user.id
    ).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")
    
    return post

@router.put("/{post_id}/publish")
async def publish_post(
    post_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Публикация поста"""
    post = db.query(PostModel).filter(
        PostModel.id == post_id,
        PostModel.user_id == current_user.id
    ).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")
    
    post.is_published = True
    post.published_at = datetime.now()
    db.commit()
    
    return {"message": "Пост успешно опубликован"}
