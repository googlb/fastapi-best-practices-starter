from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.exceptions import (
    NotFoundException,
    PermissionException,
)
from app.core.resp import PageInfo, Result
from app.dependencies.auth import get_current_user
from app.dependencies.database import get_session
from app.dependencies.pagination import PageDep
from app.dependencies.permission import Perms
from app.system.crud.crud_user import crud_user
from app.system.models import SysUser
from app.system.schemas.user import SysUserCreate, SysUserResponse, SysUserUpdate
from app.system.services.user_service import sys_user_service

router = APIRouter()


@router.get("/me", summary="获取当前用户信息", response_model=Result[SysUserResponse])
async def get_current_user_info(
    current_user: SysUser = Depends(get_current_user),
) -> Result[SysUserResponse]:
    """
    获取当前登录用户的详细信息
    无需特定权限标识，登录即可访问
    """
    user_response = SysUserResponse.model_validate(current_user)
    return Result.success(user_response)


@router.get(
    "",
    summary="获取用户列表",
    response_model=Result[PageInfo[SysUserResponse]],
    dependencies=[Depends(Perms("system:user:list"))],
)
async def get_user_list(
    *,
    session: AsyncSession = Depends(get_session),
    pagination: PageDep,
    current_user: SysUser = Depends(get_current_user),
) -> Result[PageInfo[SysUserResponse]]:
    """
    分页获取用户列表
    需要权限: system:user:list

    业务异常会被全局异常处理器自动捕获并转换为统一的 Result 格式。
    """
    page_info = await sys_user_service.get_user_page(
        session=session,
        page=pagination.page,
        size=pagination.size,
        current_user=current_user,
    )
    return Result.success(page_info)


@router.post(
    "",
    summary="创建用户",
    response_model=Result[SysUserResponse],
    dependencies=[Depends(Perms("system:user:add"))],
)
async def create_user(
    *,
    session: AsyncSession = Depends(get_session),
    user_in: SysUserCreate,
) -> Result[SysUserResponse]:
    """
    创建新用户
    需要权限: system:user:add

    业务异常会被全局异常处理器自动捕获并转换为统一的 Result 格式。
    """
    user = await sys_user_service.create_user(session, user_in)
    user_response = SysUserResponse.model_validate(user)
    return Result.success(user_response)


@router.put(
    "/{user_id}",
    summary="更新用户",
    response_model=Result[SysUserResponse],
    dependencies=[Depends(Perms("system:user:update"))],
)
async def update_user(
    *,
    session: AsyncSession = Depends(get_session),
    user_id: int,
    user_in: SysUserUpdate,
) -> Result[SysUserResponse]:
    """
    更新用户信息
    需要权限: system:user:update

    业务异常会被全局异常处理器自动捕获并转换为统一的 Result 格式。
    """
    # 1. 查出目标用户
    target_user = await crud_user.get(session, user_id)
    if not target_user:
        raise NotFoundException("用户不存在")

    # 2. 🛡️ 业务保护逻辑：保护 Admin 账号
    if target_user.username == "admin":
        # 禁止禁用 Admin
        if user_in.is_active is False:
            raise PermissionException("系统超级管理员(admin)不允许被禁用")

        # 禁止取消 Admin 的超级管理员身份
        if user_in.is_superuser is False:
            raise PermissionException("无法取消系统管理员的超级权限")

    # 3. 执行更新
    user = await sys_user_service.update_user(session, user_id, user_in)
    user_response = SysUserResponse.model_validate(user)
    return Result.success(user_response)


@router.get(
    "/{user_id}",
    summary="获取用户详情",
    response_model=Result[SysUserResponse],
    dependencies=[Depends(Perms("system:user:query"))],
)
async def get_user(
    *,
    session: AsyncSession = Depends(get_session),
    user_id: int,
) -> Result[SysUserResponse]:
    """
    根据ID获取用户详情
    需要权限: system:user:query

    业务异常会被全局异常处理器自动捕获并转换为统一的 Result 格式。
    """
    user = await crud_user.get(session, user_id)
    if not user:
        raise NotFoundException("用户不存在")

    user_response = SysUserResponse.model_validate(user)
    return Result.success(user_response)


@router.delete(
    "/{user_id}",
    summary="删除用户",
    response_model=Result,
    dependencies=[Depends(Perms("system:user:delete"))],
)
async def delete_user(
    *,
    session: AsyncSession = Depends(get_session),
    user_id: int,
    current_user: SysUser = Depends(get_current_user),
) -> Result[str]:
    """
    删除用户
    需要权限: system:user:delete

    业务异常会被全局异常处理器自动捕获并转换为统一的 Result 格式。
    """
    # 1. 查出目标用户
    user = await crud_user.get(session, user_id)
    if not user:
        raise NotFoundException("用户不存在")

    if user.username == "admin":
        raise PermissionException("系统超级管理员(admin)不允许被删除")

    if user.id == current_user.id:
        raise PermissionException("无法删除当前登录账号")

    # 4. 执行删除
    await crud_user.delete(session, id=user_id)
    return Result.success("用户删除成功")
