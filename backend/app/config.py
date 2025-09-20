import os
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Загружаем основные переменные окружения
load_dotenv()

# Загружаем переменные из .env.gpt, если файл существует
gpt_env_path = Path(__file__).parent.parent / '.env.gpt'
if gpt_env_path.exists():
    load_dotenv(gpt_env_path)

class Settings(BaseSettings):
    secret_key: str = Field(default="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=30)
    database_url: str = Field(default="postgresql://postgres:password@db:5432/marketolog")
    openai_api_key: str = Field(default="YA_PIDORAS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()