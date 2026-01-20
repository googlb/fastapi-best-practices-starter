from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List

from app.dependencies.database import get_session
from app.system.crud.crud_role import crud_role
from app.system.crud.crud_role_menu import crud_role_menu
from app.system.models import SysUser, SysMenu
from app.dependencies.auth import get_current_active_user
from app.core.resp import Result

router = APIRouter()


@router.get("/{role_id}/menus", response_model=Result[List[SysMenu]])
async def get_role_menus(
    role_id: int,
    session: AsyncSession = Depends(get_session),
) -> Result[List[SysMenu]]:
    """获取指定角色拥有的菜单列表"""
    # 检查角色是否存在
    role = await crud_role.get(session, role_id)
    if not role:
        return Result.error(404, "角色不存在")

    menus = await crud_role_menu.get_role_menus(session, role_id)
    return Result.success(menus)


@router.put("/{role_id}/menus", response_model=Result[str])
async def set_role_menus(
    role_id: int,
    menu_ids: List[int],
    session: AsyncSession = Depends(get_session),
) -> Result[str]:
    """为指定角色分配菜单权限"""
    # 检查角色是否存在
    role = await crud_role.get(session, role_id)
    if not role:
        return Result.error(404, "角色不存在")

    # 分配菜单
    success = await crud_role_menu.assign_menu_to_role(session, role_id, menu_ids)
    if not success:
        return Result.error(500, "分配菜单失败")

    return Result.success(msg="菜单分配成功", data="分配成功")
