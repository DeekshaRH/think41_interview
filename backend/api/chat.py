from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime

from db.database import database
from db.models import Session, Message

from sqlalchemy import insert, select

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    conversation_id: int | None = None  # Now this is session_id

class ChatResponse(BaseModel):
    conversation_id: int
    user_message: str
    ai_response: str
    timestamp: datetime

@router.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest):
    now = datetime.utcnow()

    # Check if session exists or create a new one
    if payload.conversation_id is None:
        # Create new session
        query = insert(Session).values(created_at=now)
        session_id = await database.execute(query)
    else:
        # Check if session exists
        query = select(Session).where(Session.id == payload.conversation_id)
        session = await database.fetch_one(query)
        if session is None:
            raise HTTPException(status_code=404, detail="Conversation ID not found.")
        session_id = payload.conversation_id

    user_message = payload.message
    ai_response = f"Echo: {user_message}"

    # Insert both user and AI messages
    insert_query = insert(Message)
    await database.execute_many(query=insert_query, values=[
        {
            "session_id": session_id,
            "sender": "user",
            "message": user_message,
            "timestamp": now
        },
        {
            "session_id": session_id,
            "sender": "ai",
            "message": ai_response,
            "timestamp": now
        }
    ])

    return ChatResponse(
        conversation_id=session_id,
        user_message=user_message,
        ai_response=ai_response,
        timestamp=now
    )
