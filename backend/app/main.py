from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import os
from contextlib import asynccontextmanager

from .database import engine, Base
from .routers import auth, company

# Удаляем создание таблиц через SQLAlchemy - теперь будем использовать миграции
# Base.metadata.create_all(bind=engine)
from backend.app.database import engine, Base
from backend.app.routers import auth, chatgpt_api, create_post

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Запускаем миграции при старте приложения
    migrations_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "migrations")
    alembic_ini = os.path.join(migrations_dir, "alembic.ini")
    try:
        print("Applying database migrations...")
        subprocess.run(["alembic", "-c", alembic_ini, "upgrade", "head"], check=True)
        print("Migrations completed successfully!")
    except Exception as e:
        print(f"Error applying migrations: {e}")
    yield

app = FastAPI(title="AI-маркетолог API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене нужно указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(company.router)
app.include_router(chatgpt_api.router)
app.include_router(create_post.router)

@app.get("/")
async def root():
    return {"message": "AI-маркетолог API"}

# @app.post("/create_company")
# async def create_company(company: Company):

