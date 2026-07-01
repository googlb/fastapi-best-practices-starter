from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.resp import PageInfo, Result
from app.dependencies.auth import get_current_active_user
from app.dependencies.database import get_session
from app.dependencies.pagination import PageDep
from app.system.crud.crud_role import crud_role
from app.system.models import SysUser
from app.system.schemas.role import RoleCreate, RoleResponse, RoleUpdate
from app.system.services.role_service import sys_role_service

router = APIRouter()


@router.get("", response_model=Result[PageInfo[RoleResponse]])
async def get_roles(
    pagination: PageDep,
    session: AsyncSession = Depends(get_session),
    current_user: SysUser = Depends(get_current_active_user),
) -> Result[PageInfo[RoleResponse]]:
    """获取角色列表"""
    roles, total = await crud_role.get_page(
        session, page=pagination.page, page_size=pagination.size
    )
    return Result.success_page(roles, total, pagination.page, pagination.size)


@router.get("/{role_id}", response_model=Result[RoleResponse])
async def get_role(
    role_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: SysUser = Depends(get_current_active_user),
) -> Result[RoleResponse]:
    """获取角色详情"""
    role = await crud_role.get(session, role_id)
    if not role:
        return Result.error(404, "角色不存在")
    return Result.success(role)


@router.post("/", response_model=Result[RoleResponse])
async def create_role(
    role_in: RoleCreate,
    session: AsyncSession = Depends(get_session),
    current_user: SysUser = Depends(get_current_active_user),
) -> Result[RoleResponse]:
    """创建角色"""
    new_role = await sys_role_service.create_role(session, role_in)
    return Result.success(new_role)


@router.put("/{role_id}", response_model=Result[RoleResponse])
async def update_role(
    role_id: int,
    role_in: RoleUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: SysUser = Depends(get_current_active_user),
) -> Result[RoleResponse]:
    """更新角色"""
    updated_role = await sys_role_service.update_role(session, role_id, role_in)
    return Result.success(updated_role)


@router.delete("/{role_id}", response_model=Result[str])
async def delete_role(
    role_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: SysUser = Depends(get_current_active_user),
) -> Result[str]:
    """删除角色"""
    await sys_role_service.delete_role(session, role_id)
    return Result.success("角色删除成功")
