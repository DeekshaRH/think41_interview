from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db.database import get_db
from db import models
from api.llm import ask_groq_llm

router = APIRouter()

class ChatRequest(BaseModel):
    user_id: int
    message: str
    session_id: int | None = None

@router.post("/chat")
def chat_endpoint(req: ChatRequest, db: Session = Depends(get_db)):
    # Session logic
    if req.session_id:
        session = db.query(models.Session).filter(models.Session.id == req.session_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
    else:
        session = models.Session(user_id=req.user_id)
        db.add(session)
        db.commit()
        db.refresh(session)

    # Save user message
    user_message = models.Message(sender="user", message=req.message, session_id=session.id)
    db.add(user_message)
    db.commit()
    db.refresh(user_message)

    # Get AI response
    messages = [
        {"role": "system", "content": "You are a helpful assistant for a shopping website."},
        {"role": "user", "content": req.message}
    ]

    try:
        ai_response = ask_groq_llm(messages)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Save AI message
    ai_message = models.Message(sender="ai", message=ai_response, session_id=session.id)
    db.add(ai_message)
    db.commit()

    return {
        "session_id": session.id,
        "user_message": req.message,
        "ai_response": ai_response
    }
