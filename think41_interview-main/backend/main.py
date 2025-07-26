# backend/main.py

from fastapi import FastAPI
from api import routes
from db.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware

# Initialize DB tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="AI Chat API",
    version="1.0"
)

# Allow frontend to connect (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(routes.router)
