from fastapi import FastAPI
from app.api.chat import router as chat_router
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
)

app.include_router(chat_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "AI Travel Planning Assistant is running"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }