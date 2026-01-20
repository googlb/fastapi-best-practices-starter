from typing import Optional, List

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.resp import Result, PageInfo
from app.dependencies.auth import get_current_user
from app.dependencies.database import get_session as get_db
from app.dependencies.pagination import PageDep
from app.system.crud.crud_menu import crud_menu
from app.system.crud.crud_role_menu import crud_role_menu
from app.system.models import SysUser, SysRole
from app.system.schemas.menu import MenuResponse, MenuCreate, MenuUpdate

router = APIRouter()


@router.get("/me", response_model=Result[List[MenuResponse]])
async def get_my_menus(
    session: AsyncSession = Depends(get_db),
    current_user: SysUser = Depends(get_current_user)
) -> Result[List[MenuResponse]]:
    """获取当前用户的菜单树"""
    if current_user.is_superuser:
        # 超级管理员拥有所有菜单
        menus = await crud_menu.get_tree(session)
    else:
        # 根据角色获取菜单
        menus = await crud_menu.get_tree_by_user(session, current_user)

    return Result.success(menus)


@router.get("", response_model=Result[PageInfo[MenuResponse]])
async def get_menus(
    pagination: PageDep,
    session: AsyncSession = Depends(get_db)
) -> Result[PageInfo[MenuResponse]]:
    """获取菜单列表"""
    menus, total = await crud_menu.get_page(
        session, page=pagination.page, page_size=pagination.size
    )
    return Result.success_page(menus, total, pagination.page, pagination.size)


@router.get("/tree", response_model=Result[List[MenuResponse]])
async def get_menu_tree(
    parent_id: Optional[int] = None,
    session: AsyncSession = Depends(get_db)
) -> Result[List[MenuResponse]]:
    """获取菜单树形结构"""
    menus = await crud_menu.get_tree(session, parent_id=parent_id)
    return Result.success(menus)


@router.get("/{menu_id}", response_model=Result[MenuResponse])
async def get_menu(
    menu_id: int,
    session: AsyncSession = Depends(get_db)
) -> Result[MenuResponse]:
    """获取菜单详情"""
    menu = await crud_menu.get(session, menu_id)
    if not menu:
        return Result.error(404, "菜单不存在")
    return Result.success(menu)


@router.get("/{menu_id}/roles", response_model=Result[List[SysRole]])
async def get_menu_roles(
    menu_id: int,
    session: AsyncSession = Depends(get_db)
) -> Result[List[SysRole]]:
    """获取菜单所属角色列表"""
    menu = await crud_menu.get(session, menu_id)
    if not menu:
        return Result.error(404, "菜单不存在")

    roles = await crud_role_menu.get_menu_roles(session, menu_id)
    return Result.success(roles)


@router.post("", response_model=Result[str])
async def create_menu(
    menu_in: MenuCreate,
    session: AsyncSession = Depends(get_db)
) -> Result[str]:
    """创建菜单"""
    await crud_menu.create(session, obj_in=menu_in)
    return Result.success("菜单创建成功")


@router.put("/{menu_id}", response_model=Result[MenuResponse])
async def update_menu(
    menu_id: int,
    menu_in: MenuUpdate,
    session: AsyncSession = Depends(get_db)
) -> Result[MenuResponse]:
    """更新菜单"""
    menu = await crud_menu.get(session, menu_id)
    if not menu:
        return Result.error(404, "菜单不存在")

    menu = await crud_menu.update(session, db_obj=menu, obj_in=menu_in)
    return Result.success(menu)


@router.delete("/{menu_id}", response_model=Result[str])
async def delete_menu(
    menu_id: int,
    session: AsyncSession = Depends(get_db)
) -> Result[str]:
    """删除菜单"""
    menu = await crud_menu.get(session, menu_id)
    if not menu:
        return Result.error(404, "菜单不存在")

    await crud_menu.delete(session, id=menu_id)
    return Result.success("Menu deleted successfully")
