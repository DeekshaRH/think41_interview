from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

# Existing Product table
class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)


# New: User table
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)

    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")


# New: Session table
class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    title = Column(String, default="New Chat")

    user = relationship("User", back_populates="sessions")
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")


# New: Message table
class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    sender = Column(String, nullable=False)  # 'user' or 'ai'
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    session = relationship("Session", back_populates="messages")
