from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from sqlalchemy.orm import Session
from openai import ChatCompletion, OpenAIError
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

openai.api_key = settings.openai_api_key

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
        
        response = ChatCompletion.create(
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
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        # Логируем неожиданные ошибки
        log_error(current_user.id, e)
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")
