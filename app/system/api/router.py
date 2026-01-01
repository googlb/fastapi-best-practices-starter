from fastapi import APIRouter
from app.system.api import user, role, menu, dict as dict_api, role_menu

api_router = APIRouter()

api_router.include_router(user.router, prefix="/users", tags=["Sys: User"])
api_router.include_router(role.router, prefix="/roles", tags=["Sys: Role"])
api_router.include_router(menu.router, prefix="/menus", tags=["Sys: Menu"])
api_router.include_router(dict_api.router, prefix="/dicts", tags=["Sys: Dict"])
api_router.include_router(role_menu.router, prefix="/roles", tags=["Sys: Role"])
