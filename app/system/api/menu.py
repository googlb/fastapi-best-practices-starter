
from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.resp import PageInfo, Result
from app.dependencies.auth import get_current_user
from app.dependencies.database import get_session as get_db
from app.dependencies.pagination import PageDep
from app.system.crud.crud_menu import crud_menu
from app.system.models import SysRole, SysUser
from app.system.schemas.menu import MenuCreate, MenuResponse, MenuUpdate
from app.system.services.menu_service import sys_menu_service

router = APIRouter()


@router.get("/me", response_model=Result[list[MenuResponse]])
async def get_my_menus(
    session: AsyncSession = Depends(get_db),
    current_user: SysUser = Depends(get_current_user),
) -> Result[list[MenuResponse]]:
    """获取当前用户的菜单树"""
    menus = await sys_menu_service.get_user_menu_tree(session, current_user)
    return Result.success(menus)


@router.get("", response_model=Result[PageInfo[MenuResponse]])
async def get_menus(
    pagination: PageDep, session: AsyncSession = Depends(get_db)
) -> Result[PageInfo[MenuResponse]]:
    """获取菜单列表"""
    menus, total = await crud_menu.get_page(
        session, page=pagination.page, page_size=pagination.size
    )
    return Result.success_page(menus, total, pagination.page, pagination.size)


@router.get("/tree", response_model=Result[list[MenuResponse]])
async def get_menu_tree(
    parent_id: int | None = None, session: AsyncSession = Depends(get_db)
) -> Result[list[MenuResponse]]:
    """获取菜单树形结构"""
    menus = await crud_menu.get_tree(session, parent_id=parent_id)
    return Result.success(menus)


@router.get("/{menu_id}", response_model=Result[MenuResponse])
async def get_menu(
    menu_id: int, session: AsyncSession = Depends(get_db)
) -> Result[MenuResponse]:
    """获取菜单详情"""
    menu = await crud_menu.get(session, menu_id)
    if not menu:
        return Result.error(404, "菜单不存在")
    return Result.success(menu)


@router.get("/{menu_id}/roles", response_model=Result[list[SysRole]])
async def get_menu_roles(
    menu_id: int, session: AsyncSession = Depends(get_db)
) -> Result[list[SysRole]]:
    """获取菜单所属角色列表"""
    roles = await sys_menu_service.get_menu_roles(session, menu_id)
    return Result.success(roles)


@router.post("", response_model=Result[str])
async def create_menu(
    menu_in: MenuCreate, session: AsyncSession = Depends(get_db)
) -> Result[str]:
    """创建菜单"""
    await sys_menu_service.create_menu(session, menu_in)
    return Result.success("菜单创建成功")


@router.put("/{menu_id}", response_model=Result[MenuResponse])
async def update_menu(
    menu_id: int, menu_in: MenuUpdate, session: AsyncSession = Depends(get_db)
) -> Result[MenuResponse]:
    """更新菜单"""
    menu = await sys_menu_service.update_menu(session, menu_id, menu_in)
    return Result.success(menu)


@router.delete("/{menu_id}", response_model=Result[str])
async def delete_menu(
    menu_id: int, session: AsyncSession = Depends(get_db)
) -> Result[str]:
    """删除菜单"""
    await sys_menu_service.delete_menu(session, menu_id)
    return Result.success("菜单删除成功")
