from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from .routers import auth, company

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
app.include_router(company.router)

@app.get("/")
async def root():
    return {"message": "AI-маркетолог API"}

# @app.post("/create_company")
# async def create_company(company: Company):

