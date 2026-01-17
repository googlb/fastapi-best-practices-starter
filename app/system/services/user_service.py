from sqlalchemy.orm import selectinload
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime, timezone
from typing import Optional, List

from app.system.crud.crud_user import crud_user
from app.system.models import SysUser
from app.system.schemas.user import SysUserCreate, SysUserUpdate, SysUserResponse
from app.core.resp import Result


class SysUserService:
    async def create_user(self, session: AsyncSession, obj_in: SysUserCreate)-> Result[SysUser]:
        """创建用户"""
        # 检查用户名是否已存在
        user = await crud_user.get_by_username(session, obj_in.username)
        if user:
            return Result.error(400, "用户名已存在")

        # 检查邮箱是否已存在
        user = await crud_user.get_by_email(session, obj_in.email)
        if user:
            return Result.error(400, "邮箱已存在")

        # 创建用户
        user = await crud_user.create(session, obj_in=obj_in)
        return Result.success(user)

    async def update_user(
        self,
        session: AsyncSession,
        user_id: int,
        obj_in: SysUserUpdate
    ) -> Result[SysUser]:
        """更新用户"""
        # 1. 查找是否存在
        db_obj = await crud_user.get(session, user_id)
        if not db_obj:
            return Result.error(404, "用户不存在")

        # 2. 检查邮箱唯一性 (如果修改了邮箱)
        if obj_in.email and obj_in.email != db_obj.email:
            if await crud_user.get_by_email(session, obj_in.email):
                return Result.error(400, "邮箱已存在")

        user = await crud_user.update(
            session,
            db_obj=db_obj,
            obj_in=obj_in
        )

        return Result.success(user)

    async def update_last_login(
        self,
        session: AsyncSession,
        user_id: int
    ) -> Result[SysUser]:
        """更新最后登录时间"""
        user = await crud_user.get(session, user_id)
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
    ) -> Result[SysUser]:
        """验证用户"""
        user = await crud_user.authenticate(session, username, password)
        if not user:
            return Result.error(401, "用户名或密码错误")

        if not user.is_active:
            return Result.error(403, "用户已被禁用")

        # 更新最后登录时间
        user.last_login_at = datetime.now(timezone.utc)
        session.add(user)
        await session.commit()
        await session.refresh(user)

        return Result.success(user)

    async def get_user_page(
        self,
        session: AsyncSession,
        page: int,
        size: int,
        current_user: SysUser,
    ) -> Result[PageInfo[SysUserResponse]]:
        if not current_user.is_superuser:
            return Result.error(403, "权限不足")

        # 传入 selectinload，解决 MissingGreenlet 错误
        users, total = await crud_user.get_page(
            session,
            page=page,
            page_size=size,
            options=[selectinload(SysUser.roles)]
        )

        # 后续逻辑保持不变 (手动提取 role_ids)
        user_responses = []
        for user in users:
            role_ids = [role.id for role in user.roles]

            # 使用 model_validate 转换
            # (确保 SysUserResponse 允许 extra fields 或者手动构建 dict)
            user_resp = SysUserResponse.model_validate(user)
            user_resp.role_ids = role_ids

            user_responses.append(user_resp)

        return Result.success_page(
            items=user_responses,
            total=total,
            page=page,
            size=size
        )


sys_user_service = SysUserService()
