"""
Routes package for the ASU Chatbot API

This package contains all API route definitions and handlers.
"""

from fastapi import APIRouter
from .chat import router as chat_router
from .auth import router as auth_router

# Create main API router
api_router = APIRouter()

# Include all route modules
api_router.include_router(
    chat_router, 
    prefix="/chat", 
    tags=["chat"]
)

api_router.include_router(
    auth_router,
    prefix="/auth",
    tags=["authentication"]
)

# Export the main router
__all__ = ["api_router"]