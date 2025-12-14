from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import timedelta
from uuid import UUID

from app.dependencies.database import get_session
from app.dependencies.auth import get_current_user
from app.system.schemas.user import (
    SysUserCreate, 
    SysUserUpdate, 
    SysUserResponse, 
    UserLogin, 
    TokenResponse
)
from app.system.crud.crud_user import crud_sys_user
from app.system.services.user_service import sys_user_service
from app.core.security import create_access_token, create_refresh_token
from app.system.models import SysUser
from app.core.result import Result

router = APIRouter(prefix="/users", tags=["系统-用户"])


@router.post("/login")
async def login(
    credentials: UserLogin,
    session: AsyncSession = Depends(get_session),
):
    """用户登录"""
    result = await sys_user_service.authenticate_user(
        session, credentials.username, credentials.password
    )
    
    if not result.success:
        return result
    
    user = result.data
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    return Result.success({
        "access_token": access_token,
        "refresh_token": refresh_token,
    })


@router.get("/me")
async def get_current_user_info(
    current_user: SysUser = Depends(get_current_user),
):
    """获取当前用户信息"""
    return Result.success(current_user)


@router.post("/")
async def create_user(
    *,
    session: AsyncSession = Depends(get_session),
    user_in: SysUserCreate,
    current_user: SysUser = Depends(get_current_user)
):
    """创建用户"""
    if not current_user.is_superuser:
        return Result.error(403, "权限不足")
    
    result = await sys_user_service.create_user(session, user_in)
    
    if not result.success:
        return result
    
    return result


@router.put("/{user_id}")
async def update_user(
    *,
    session: AsyncSession = Depends(get_session),
    user_id: UUID,
    user_in: SysUserUpdate,
    current_user: SysUser = Depends(get_current_user)
):
    """更新用户"""
    if not current_user.is_superuser and current_user.id != user_id:
        return Result.error(403, "权限不足")
    
    result = await sys_user_service.update_user(session, user_id, user_in)
    
    if not result.success:
        return result
    
    return result


@router.get("/{user_id}")
async def get_user(
    *,
    session: AsyncSession = Depends(get_session),
    user_id: UUID,
    current_user: SysUser = Depends(get_current_user)
):
    """获取用户详情"""
    if not current_user.is_superuser and current_user.id != user_id:
        return Result.error(403, "权限不足")
    
    user = await crud_sys_user.get(session, user_id)
    if not user:
        return Result.error(404, "用户不存在")
    
    return Result.success(user)


@router.delete("/{user_id}")
async def delete_user(
    *,
    session: AsyncSession = Depends(get_session),
    user_id: UUID,
    current_user: SysUser = Depends(get_current_user)
):
    """删除用户"""
    if not current_user.is_superuser:
        return Result.error(403, "权限不足")
    
    user = await crud_sys_user.delete(session, user_id)
    if not user:
        return Result.error(404, "用户不存在")
    
    return Result.success({"message": "用户删除成功"})
