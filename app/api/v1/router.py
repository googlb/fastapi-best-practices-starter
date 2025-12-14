from fastapi import APIRouter

# Import routers from new structure
from app.system.api.router import api_router as system_router
from app.business.api.router import api_router as business_router

api_v1_router = APIRouter()

api_v1_router.include_router(system_router, prefix="/system")
api_v1_router.include_router(business_router, prefix="/api")
