from fastapi import APIRouter
from app.business.api import business

api_router = APIRouter()
api_router.include_router(business.router, prefix="/business", tags=["业务模块"])
