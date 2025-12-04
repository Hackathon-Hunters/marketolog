import httpx
import base64
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.models import Company as CompanyModel, User as UserModel
from ..utils.auth import get_current_active_user
from ..schemas.company import TelegramSettings

router = APIRouter(
    prefix="/telegram",
    tags=["telegram"],
)

TELEGRAM_API_URL = "https://api.telegram.org/bot"


class SendPostRequest(BaseModel):
    company_id: int
    title: Optional[str] = None
    description: str
    hashtags: Optional[List[str]] = None
    image_base64: Optional[str] = None


class TelegramResponse(BaseModel):
    success: bool
    message: str


async def send_telegram_message(
    bot_token: str,
    chat_id: str,
    text: str,
    image_base64: Optional[str] = None
) -> dict:
    """Отправка сообщения в Telegram"""
    async with httpx.AsyncClient() as client:
        if image_base64:
            # Отправка фото с подписью
            image_data = base64.b64decode(image_base64)
            files = {"photo": ("image.jpg", image_data, "image/jpeg")}
            data = {"chat_id": chat_id, "caption": text, "parse_mode": "HTML"}
            
            response = await client.post(
                f"{TELEGRAM_API_URL}{bot_token}/sendPhoto",
                data=data,
                files=files,
                timeout=30.0
            )
        else:
            # Отправка только текста
            data = {
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "HTML"
            }
            response = await client.post(
                f"{TELEGRAM_API_URL}{bot_token}/sendMessage",
                json=data,
                timeout=30.0
            )
        
        return response.json()


@router.post("/send", response_model=TelegramResponse)
async def send_post_to_telegram(
    request: SendPostRequest,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Отправка поста в Telegram канал/чат"""
    # Получаем компанию пользователя
    company = db.query(CompanyModel).filter(
        CompanyModel.id == request.company_id,
        CompanyModel.user_id == current_user.id
    ).first()
    
    if not company:
        raise HTTPException(status_code=404, detail="Компания не найдена")
    
    if not company.telegram_bot_token or not company.telegram_chat_id:
        raise HTTPException(
            status_code=400, 
            detail="Настройки Telegram не заполнены. Укажите токен бота и Chat ID в настройках компании."
        )
    
    # Формируем текст сообщения
    text_parts = []
    
    if request.title:
        text_parts.append(f"<b>{request.title}</b>")
    
    text_parts.append(request.description)
    
    if request.hashtags:
        hashtags_text = " ".join(request.hashtags)
        text_parts.append(f"\n{hashtags_text}")
    
    full_text = "\n\n".join(text_parts)
    
    # Отправляем в Telegram
    try:
        result = await send_telegram_message(
            bot_token=company.telegram_bot_token,
            chat_id=company.telegram_chat_id,
            text=full_text,
            image_base64=request.image_base64
        )
        
        if result.get("ok"):
            return TelegramResponse(success=True, message="Пост успешно отправлен в Telegram")
        else:
            error_description = result.get("description", "Неизвестная ошибка")
            raise HTTPException(status_code=400, detail=f"Ошибка Telegram API: {error_description}")
            
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Превышено время ожидания ответа от Telegram")
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Ошибка соединения с Telegram: {str(e)}")


@router.put("/settings/{company_id}", response_model=TelegramResponse)
async def update_telegram_settings(
    company_id: int,
    settings: TelegramSettings,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Обновление настроек Telegram для компании"""
    company = db.query(CompanyModel).filter(
        CompanyModel.id == company_id,
        CompanyModel.user_id == current_user.id
    ).first()
    
    if not company:
        raise HTTPException(status_code=404, detail="Компания не найдена")
    
    if settings.telegram_bot_token is not None:
        company.telegram_bot_token = settings.telegram_bot_token
    
    if settings.telegram_chat_id is not None:
        company.telegram_chat_id = settings.telegram_chat_id
    
    db.commit()
    
    return TelegramResponse(success=True, message="Настройки Telegram успешно обновлены")


@router.get("/settings/{company_id}")
async def get_telegram_settings(
    company_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Получение настроек Telegram для компании"""
    company = db.query(CompanyModel).filter(
        CompanyModel.id == company_id,
        CompanyModel.user_id == current_user.id
    ).first()
    
    if not company:
        raise HTTPException(status_code=404, detail="Компания не найдена")
    
    # Маскируем токен для безопасности
    masked_token = None
    if company.telegram_bot_token:
        token = company.telegram_bot_token
        masked_token = token[:8] + "..." + token[-4:] if len(token) > 12 else "***"
    
    return {
        "telegram_bot_token": masked_token,
        "telegram_chat_id": company.telegram_chat_id,
        "is_configured": bool(company.telegram_bot_token and company.telegram_chat_id)
    }


@router.post("/test/{company_id}", response_model=TelegramResponse)
async def test_telegram_connection(
    company_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Тестирование подключения к Telegram"""
    company = db.query(CompanyModel).filter(
        CompanyModel.id == company_id,
        CompanyModel.user_id == current_user.id
    ).first()
    
    if not company:
        raise HTTPException(status_code=404, detail="Компания не найдена")
    
    if not company.telegram_bot_token or not company.telegram_chat_id:
        raise HTTPException(
            status_code=400, 
            detail="Настройки Telegram не заполнены"
        )
    
    try:
        result = await send_telegram_message(
            bot_token=company.telegram_bot_token,
            chat_id=company.telegram_chat_id,
            text="✅ Тестовое сообщение от Marketolog\n\nПодключение настроено успешно!"
        )
        
        if result.get("ok"):
            return TelegramResponse(success=True, message="Тестовое сообщение успешно отправлено!")
        else:
            error_description = result.get("description", "Неизвестная ошибка")
            raise HTTPException(status_code=400, detail=f"Ошибка: {error_description}")
            
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Превышено время ожидания")
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Ошибка соединения: {str(e)}")

