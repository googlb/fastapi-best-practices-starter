from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime
from typing import Optional

from app.system.crud.crud_user import crud_sys_user
from app.system.schemas.user import SysUserCreate, SysUserUpdate
from app.core.resp import Result


class SysUserService:
    async def create_user(self, session: AsyncSession, obj_in: SysUserCreate):
        """创建用户"""
        # 检查用户名是否已存在
        user = await crud_sys_user.get_by_username(session, obj_in.username)
        if user:
            return Result.error(400, "用户名已存在")
        
        # 检查邮箱是否已存在
        user = await crud_sys_user.get_by_email(session, obj_in.email)
        if user:
            return Result.error(400, "邮箱已存在")
        
        # 创建用户
        user = await crud_sys_user.create(session, obj_in)
        return Result.success(user)
    
    async def update_user(
        self, 
        session: AsyncSession, 
        user_id: int, 
        obj_in: SysUserUpdate
    ):
        """更新用户"""
        user = await crud_sys_user.get(session, user_id)
        if not user:
            return Result.error(404, "用户不存在")
        
        # 如果更新用户名，检查是否已存在
        if obj_in.username and obj_in.username != user.username:
            existing_user = await crud_sys_user.get_by_username(session, obj_in.username)
            if existing_user:
                return Result.error(400, "用户名已存在")
        
        # 如果更新邮箱，检查是否已存在
        if obj_in.email and obj_in.email != user.email:
            existing_user = await crud_sys_user.get_by_email(session, obj_in.email)
            if existing_user:
                return Result.error(400, "邮箱已存在")
        
        # 更新用户
        user = await crud_sys_user.update(session, user, obj_in)
        return Result.success(user)
    
    async def update_last_login(
        self, 
        session: AsyncSession, 
        user_id: int
    ):
        """更新最后登录时间"""
        user = await crud_sys_user.get(session, user_id)
        if not user:
            return Result.error(404, "用户不存在")
        
        user.last_login_at = datetime.utcnow()
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return Result.success(user)
    
    async def authenticate_user(
        self, 
        session: AsyncSession, 
        username: str, 
        password: str
    ):
        """验证用户"""
        user = await crud_sys_user.authenticate(session, username, password)
        if not user:
            return Result.error(401, "用户名或密码错误")
        
        if not user.is_active:
            return Result.error(403, "用户已被禁用")
        
        # 更新最后登录时间
        await self.update_last_login(session, user.id)
        
        return Result.success(user)


sys_user_service = SysUserService()
