from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.database import engine, Base
from backend.app.routers import auth, chatgpt_api, create_post

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI-маркетолог API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене нужно указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(chatgpt_api.router)
app.include_router(create_post.router)

@app.get("/")
async def root():
    return {"message": "AI-маркетолог API"} 