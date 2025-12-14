from fastapi import APIRouter

# Import routers from new structure
from app.system.api.router import api_router as system_router

api_v1_router = APIRouter()

api_v1_router.include_router(system_router, prefix="/sys")
