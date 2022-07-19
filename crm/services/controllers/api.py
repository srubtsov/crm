from fastapi import APIRouter

from .user import auth

api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"], prefix="/auth")
