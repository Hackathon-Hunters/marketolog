from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from sqlalchemy.orm import Session
from openai import OpenAI, OpenAIError
import openai
import logging
import json
from datetime import datetime

from ..utils.auth import get_current_active_user
from ..models.models import User as UserModel
from ..config import settings

# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Создаем форматтер для логов
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Создаем обработчик для записи в файл
file_handler = logging.FileHandler('chatgpt_api.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

router = APIRouter(
    prefix="/ai-requests",
    tags=["ai-requests"],
)

# Проверка наличия API ключа
if not settings.openai_api_key:
    logger.error("OpenAI API key is not set! Please check .env.gpt file")
    raise ValueError("OpenAI API key is not set! Please check .env.gpt file")

# Инициализация клиента OpenAI
client = OpenAI(api_key=settings.openai_api_key)
logger.info(f"OpenAI API key loaded: {settings.openai_api_key[:8]}...")

class Message(BaseModel):
    role: str = Field(..., description="Роль отправителя (user/assistant/system)")
    content: str = Field(..., description="Содержание сообщения")

class ChatRequest(BaseModel):
    messages: List[Message] = Field(..., description="История сообщений")
    model: str = Field(default="gpt-3.5-turbo", description="Модель GPT")
    temperature: float = Field(default=0.7, ge=0, le=2, description="Температура генерации")
    max_tokens: Optional[int] = Field(default=None, description="Максимальное количество токенов в ответе")

def log_request(user_id: int, request_data: dict):
    """Логирование входящего запроса"""
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "user_id": user_id,
        "request": request_data
    }
    logger.info(f"ChatGPT Request: {json.dumps(log_data, ensure_ascii=False)}")

def log_response(user_id: int, response_data: dict):
    """Логирование ответа"""
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "user_id": user_id,
        "response": response_data
    }
    logger.info(f"ChatGPT Response: {json.dumps(log_data, ensure_ascii=False)}")

def log_error(user_id: int, error: Exception):
    """Логирование ошибки"""
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "user_id": user_id,
        "error": str(error),
        "error_type": type(error).__name__
    }
    logger.error(f"ChatGPT Error: {json.dumps(log_data, ensure_ascii=False)}")

@router.post("/chat")
async def chat_with_gpt(
    chat_request: ChatRequest,
    current_user: UserModel = Depends(get_current_active_user)
):
    try:
        # Логируем входящий запрос
        log_request(current_user.id, chat_request.dict())
        
        # Проверяем наличие сообщений
        if not chat_request.messages:
            raise HTTPException(status_code=400, detail="Messages list cannot be empty")
        
        # Проверяем валидность ролей
        valid_roles = {"system", "user", "assistant"}
        for msg in chat_request.messages:
            if msg.role not in valid_roles:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Invalid role: {msg.role}. Must be one of: {', '.join(valid_roles)}"
                )
        
        # Создаем запрос к ChatGPT
        response = client.chat.completions.create(
            model=chat_request.model,
            messages=[msg.dict() for msg in chat_request.messages],
            temperature=chat_request.temperature,
            max_tokens=chat_request.max_tokens
        )
        
        response_data = {"response": response.choices[0].message.content}
        
        # Логируем успешный ответ
        log_response(current_user.id, response_data)
        
        return response_data
        
    except OpenAIError as e:
        # Логируем ошибку API
        log_error(current_user.id, e)
        error_message = str(e)
        
        # Обработка различных типов ошибок
        if "API key" in error_message:
            raise HTTPException(
                status_code=500,
                detail="Invalid OpenAI API key. Please check your .env.gpt file"
            )
        elif "insufficient_quota" in error_message:
            raise HTTPException(
                status_code=429,
                detail="OpenAI API quota exceeded. Please check your billing details at https://platform.openai.com/account/billing"
            )
        elif "rate_limit" in error_message:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please try again later"
            )
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        # Логируем неожиданные ошибки
        log_error(current_user.id, e)
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")
