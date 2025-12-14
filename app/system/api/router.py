from fastapi import APIRouter
from app.system.api import user, role, menu, dict as dict_api

api_router = APIRouter()

api_router.include_router(user.router, prefix="/users", tags=["系统-用户"])
api_router.include_router(role.router, prefix="/roles", tags=["系统-角色"])
api_router.include_router(menu.router, prefix="/menus", tags=["系统-菜单"])
api_router.include_router(dict_api.router, prefix="/dicts", tags=["系统-字典"])
