# backend/api/routes.py
from fastapi import APIRouter
from api.chat import router as chat_router

router = APIRouter()

router.include_router(chat_router)

@router.get("/ping")
def ping():
    return {"message": "pong"}
