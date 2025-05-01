from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from openai import OpenAI, OpenAIError
import openai
import logging
import json
from datetime import datetime
import base64
import requests

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

class IdeaGenerationRequest(BaseModel):
    company_name: str = Field(..., description="Название компании")
    business_type: str = Field(..., description="Род деятельности компании")
    region: str = Field(..., description="Регион деятельности")
    language: str = Field(..., description="Язык для перевода")
    model: str = Field(default="gpt-3.5-turbo", description="Модель GPT")
    temperature: float = Field(default=0.7, ge=0, le=2, description="Температура генерации")

class PostGenerationRequest(BaseModel):
    prompt: str = Field(..., description="Краткое описание/промпт для генерации поста")

class IdeaResponse(BaseModel):
    title: str = Field(..., description="Название идеи")
    description: str = Field(..., description="Описание идеи")
    benefits: List[str] = Field(..., description="Преимущества идеи")
    hashtags: List[str] = Field(..., description="Хештеги для соц. сетей")
    image_prompt: str = Field(..., description="Промпт для генерации изображения")
    image_base64: Optional[str] = Field(None, description="Изображение в формате base64")

class PostResponse(BaseModel):
    title: str = Field(..., description="Заголовок поста")
    description: str = Field(..., description="Содержание поста")
    hashtags: List[str] = Field(..., description="Хештеги для соц. сетей")
    image_base64: Optional[str] = Field(None, description="Изображение в формате base64")

class IdeasGenerationResponse(BaseModel):
    ideas: List[IdeaResponse] = Field(..., description="Список идей")

def log_request(user_id: int, request_data: Any):
    """Логирование входящего запроса"""
    # Преобразуем Pydantic модель в словарь, если она передана
    if hasattr(request_data, "dict"):
        request_data = request_data.dict()
        
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "user_id": user_id,
        "request": request_data
    }
    logger.info(f"ChatGPT Request: {json.dumps(log_data, ensure_ascii=False)}")

def log_response(user_id: int, response_data: Any):
    """Логирование ответа"""
    # Преобразуем Pydantic модель в словарь, если она передана
    if hasattr(response_data, "dict"):
        response_data = response_data.dict()
        
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

async def generate_image(prompt: str) -> str:
    """Генерация изображения через DALL-E"""
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        
        # Скачиваем изображение и конвертируем в base64
        image_response = requests.get(image_url)
        image_response.raise_for_status()
        return base64.b64encode(image_response.content).decode('utf-8')
    except Exception as e:
        logger.error(f"Error generating image: {str(e)}")
        return None

@router.post("/generate-ideas", response_model=IdeasGenerationResponse)
async def generate_ideas(
    current_user: UserModel = Depends(get_current_active_user)
):
    company = current_user.company
    try:
        # Логируем входящий запрос
        
        # Создаем промпт для генерации идей
        prompt_template = f"""
        Ты - профессиональный бизнес-консультант по маркетингу. 
        
        Компания: {company.name}
        Род деятельности: {company.industry}
        Регион: {company.region}
        Язык: Русский
        
        Сгенерируй ТОП-3 маркетинговые идеи для постов в соц. сетях этой компании, которые помогут повысить узнаваемость бренда и привлечь новых клиентов.
        
        Для каждой идеи также:
        1. Добавь 5-7 релевантных хештегов для соц. сетей
        2. Создай промпт для генерации изображения, которое будет иллюстрировать идею
        
        Твой ответ должен быть ТОЛЬКО в формате JSON со следующей структурой:
        {{
            "ideas": [
                {{
                    "title": "Название идеи",
                    "description": "Подробное описание идеи",
                    "benefits": ["Преимущество 1", "Преимущество 2", "Преимущество 3"],
                    "hashtags": ["#хештег1", "#хештег2", ...],
                    "image_prompt": "Детальное описание изображения для генерации"
                }},
                ... (всего 3 идеи)
            ]
        }}
        
        НЕ ДОБАВЛЯЙ никаких пояснений или дополнительного текста вне этой JSON структуры.
        """
        
        # Отправляем запрос к ChatGPT
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt_template}],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        
        # Получаем ответ и преобразуем его в JSON
        response_content = response.choices[0].message.content
        ideas_data = json.loads(response_content)
        
        # # Генерируем изображения для каждой идеи
        # for idea in ideas_data["ideas"]:
        #     image_base64 = await generate_image(idea["image_prompt"])
        #     print(image_base64)
        #     idea["image_base64"] = image_base64
        
        # Формируем структурированный ответ
        response_data = IdeasGenerationResponse(**ideas_data)
        
        # Логируем успешный ответ
        log_response(current_user.id, ideas_data)
        
        return response_data
        
    except json.JSONDecodeError as e:
        log_error(current_user.id, e)
        raise HTTPException(
            status_code=500,
            detail="Не удалось распарсить ответ от API в формате JSON"
        )
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

@router.post("/generate-post", response_model=PostResponse)
async def generate_post(
    request: PostGenerationRequest,
    current_user: UserModel = Depends(get_current_active_user)
):
    try:
        # Логируем входящий запрос
        log_request(current_user.id, request)
        
        # Создаем промпт для генерации поста
        prompt_template = f"""
        Ты - профессиональный копирайтер и маркетолог.
        
        На основе этого промпта: "{request.prompt}"
        
        Создай привлекательный пост для социальных сетей, который привлечет внимание аудитории.
        
        Твой ответ должен быть ТОЛЬКО в формате JSON со следующей структурой:
        {{
            "title": "Привлекательный заголовок поста",
            "description": "Детальное содержание поста в несколько абзацев",
            "hashtags": ["#хештег1", "#хештег2", "#хештег3", ...],
            "image_prompt": "Детальное описание изображения, которое будет иллюстрировать пост, для генерации через DALL-E"
        }}
        
        НЕ ДОБАВЛЯЙ никаких пояснений или дополнительного текста вне этой JSON структуры.
        """
        
        # Отправляем запрос к ChatGPT
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt_template}],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        
        # Получаем ответ и преобразуем его в JSON
        response_content = response.choices[0].message.content
        post_data = json.loads(response_content)
        
        # Генерируем изображение на основе prompt
        image_base64 = await generate_image(post_data["image_prompt"])
        post_data["image_base64"] = image_base64
        
        # Удаляем поле image_prompt так как оно не требуется в ответе
        post_data.pop("image_prompt", None)
        
        # Формируем структурированный ответ
        response_data = PostResponse(**post_data)
        
        # Логируем успешный ответ
        log_response(current_user.id, post_data)
        
        return response_data
        
    except json.JSONDecodeError as e:
        log_error(current_user.id, e)
        raise HTTPException(
            status_code=500,
            detail="Не удалось распарсить ответ от API в формате JSON"
        )
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
