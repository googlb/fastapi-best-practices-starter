from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID
from typing import List

from app.dependencies.database import get_session
from app.system.crud.crud_role import crud_role
from app.system.crud.crud_role_menu import crud_role_menu
from app.system.models import SysRole, SysMenu, SysUser
from app.system.schemas.role import Role, RoleCreate, RoleUpdate
from app.system.schemas.menu import Menu
from app.dependencies.auth import get_current_active_user
from app.core.resp import Result

router = APIRouter()


@router.get("/")
async def get_roles(
    page: int = 1,
    size: int = 20,
    session: AsyncSession = Depends(get_session),
    current_user: SysUser = Depends(get_current_active_user)
):
    """获取角色列表"""
    roles, total = await crud_role.get_page(session, page=page, page_size=size)
    return Result.success_page(roles, total, page, size)


@router.get("/{role_id}")
async def get_role(
    role_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: SysUser = Depends(get_current_active_user)
):
    """获取角色详情"""
    role = await crud_role.get(session, role_id)
    if not role:
        return Result.error(404, "角色不存在")
    return Result.success(role)


@router.get("/{role_id}/menus")
async def get_role_menus(
    role_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: SysUser = Depends(get_current_active_user)
):
    """获取角色拥有的菜单列表"""
    # 检查角色是否存在
    role = await crud_role.get(session, role_id)
    if not role:
        return Result.error(404, "角色不存在")
    
    menus = await crud_role_menu.get_role_menus(session, role_id)
    return Result.success(menus)


@router.post("/{role_id}/menus")
async def assign_menus_to_role(
    role_id: UUID,
    menu_ids: List[UUID],
    session: AsyncSession = Depends(get_session),
    current_user: SysUser = Depends(get_current_active_user)
):
    """为角色分配菜单"""
    # 检查角色是否存在
    role = await crud_role.get(session, role_id)
    if not role:
        return Result.error(404, "角色不存在")
    
    # 分配菜单
    success = await crud_role_menu.assign_menu_to_role(session, role_id, menu_ids)
    if not success:
        return Result.error(500, "分配菜单失败")
    
    return Result.success({"message": "菜单分配成功"})


@router.post("/{role_id}/menus/{menu_id}")
async def add_menu_to_role(
    role_id: UUID,
    menu_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: SysUser = Depends(get_current_active_user)
):
    """为角色添加单个菜单"""
    # 检查角色是否存在
    role = await crud_role.get(session, role_id)
    if not role:
        return Result.error(404, "角色不存在")
    
    # 添加菜单
    success = await crud_role_menu.add_menu_to_role(session, role_id, menu_id)
    if not success:
        return Result.error(500, "添加菜单失败")
    
    return Result.success({"message": "菜单添加成功"})


@router.delete("/{role_id}/menus/{menu_id}")
async def remove_menu_from_role(
    role_id: UUID,
    menu_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: SysUser = Depends(get_current_active_user)
):
    """从角色中移除菜单"""
    # 检查角色是否存在
    role = await crud_role.get(session, role_id)
    if not role:
        return Result.error(404, "角色不存在")
    
    # 移除菜单
    success = await crud_role_menu.delete_menu_from_role(session, role_id, menu_id)
    if not success:
        return Result.error(500, "移除菜单失败")
    
    return Result.success({"message": "菜单移除成功"})


@router.post("/")
async def create_role(
    role_in: RoleCreate,
    session: AsyncSession = Depends(get_session),
    current_user: SysUser = Depends(get_current_active_user)
):
    """创建角色"""
    # 检查角色编码是否已存在
    role = await crud_role.get_by_code(session, role_in.code)
    if role:
        return Result.error(400, "角色编码已存在")
    
    new_role = await crud_role.create(session, role_in)
    return Result.success(new_role)


@router.put("/{role_id}")
async def update_role(
    role_id: UUID,
    role_in: RoleUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: SysUser = Depends(get_current_active_user)
):
    """更新角色"""
    role = await crud_role.get(session, role_id)
    if not role:
        return Result.error(404, "角色不存在")
    
    # 如果更新编码，检查是否已存在
    if role_in.code and role_in.code != role.code:
        existing_role = await crud_role.get_by_code(session, role_in.code)
        if existing_role:
            return Result.error(400, "角色编码已存在")
    
    updated_role = await crud_role.update(session, role, role_in)
    return Result.success(updated_role)


@router.delete("/{role_id}")
async def delete_role(
    role_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: SysUser = Depends(get_current_active_user)
):
    """删除角色"""
    role = await crud_role.get(session, role_id)
    if not role:
        return Result.error(404, "角色不存在")
    
    await crud_role.delete(session, role_id)
    return Result.success({"message": "角色删除成功"})
