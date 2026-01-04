from fastapi import APIRouter

# Import routers from new structure
from app.system.api.router import api_router as system_router
from app.system.api import auth

api_v1_router = APIRouter()

# A. 注册认证模块，使用 /auth 前缀
api_v1_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Sys: Auth"]
)

api_v1_router.include_router(system_router, prefix="/sys")
