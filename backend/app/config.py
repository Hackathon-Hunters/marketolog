import os
from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    secret_key: str = Field(default="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=30)
    database_url: str = Field(default="sqlite:///./app.db")
    openai_api_key: str = Field(default="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") 

settings = Settings() 