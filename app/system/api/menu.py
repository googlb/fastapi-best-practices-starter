from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from app.dependencies.database import get_session as get_db
from app.system.models import SysMenu, SysRole
from app.system.crud.crud_menu import crud_menu
from app.system.crud.crud_role_menu import crud_role_menu
from app.core.result import Result, PageResult

router = APIRouter()


@router.get("/")
async def get_menus(
    page: int = 1,
    size: int = 20,
    session: AsyncSession = Depends(get_db)
):
    """获取菜单列表"""
    menus, total = await crud_menu.get_page(session, page=page, page_size=size)
    return PageResult.success([menu.model_dump() for menu in menus], total, page, size)


@router.get("/tree")
async def get_menu_tree(
    parent_id: Optional[UUID] = None,
    session: AsyncSession = Depends(get_db)
):
    """获取菜单树形结构"""
    menus = await crud_menu.get_tree(session, parent_id=parent_id)
    return Result.success(menus)


@router.get("/{menu_id}")
async def get_menu(
    menu_id: UUID,
    session: AsyncSession = Depends(get_db)
):
    """获取菜单详情"""
    menu = await crud_menu.get(session, menu_id)
    if not menu:
        return Result.error(404, "菜单不存在")
    return Result.success(menu)


@router.get("/{menu_id}/roles")
async def get_menu_roles(
    menu_id: UUID,
    session: AsyncSession = Depends(get_db)
):
    """获取菜单所属角色列表"""
    menu = await crud_menu.get(session, menu_id)
    if not menu:
        return Result.error(404, "菜单不存在")
    
    roles = await crud_role_menu.get_menu_roles(session, menu_id)
    return Result.success(roles)


@router.post("/")
async def create_menu(
    menu_data: dict,
    session: AsyncSession = Depends(get_db)
):
    """创建菜单"""
    menu = await crud_menu.create(session, menu_data)
    return Result.success(menu)


@router.put("/{menu_id}")
async def update_menu(
    menu_id: UUID,
    menu_data: dict,
    session: AsyncSession = Depends(get_db)
):
    """更新菜单"""
    menu = await crud_menu.get(session, menu_id)
    if not menu:
        return Result.error(404, "菜单不存在")
    
    menu = await crud_menu.update(session, menu, menu_data)
    return Result.success(menu)


@router.delete("/{menu_id}")
async def delete_menu(
    menu_id: UUID,
    session: AsyncSession = Depends(get_db)
):
    """删除菜单"""
    menu = await crud_menu.get(session, menu_id)
    if not menu:
        return Result.error(404, "菜单不存在")
    
    await crud_menu.delete(session, menu_id)
    return Result.success({"message": "Menu deleted successfully"})
