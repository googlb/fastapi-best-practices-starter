from sqlalchemy.orm import selectinload
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime, timezone

from app.system.crud.crud_user import crud_user
from app.system.models import SysUser
from app.system.schemas.user import SysUserCreate, SysUserUpdate, SysUserResponse
from app.core.resp import PageInfo
from app.core.exceptions import (
    ValidationException,
    NotFoundException,
    AuthenticationException,
    PermissionException,
)


class SysUserService:
    async def create_user(self, session: AsyncSession, obj_in: SysUserCreate) -> SysUser:
        """
        创建用户
        
        Args:
            session: 数据库会话
            obj_in: 用户创建数据
            
        Returns:
            SysUser: 创建的用户对象
            
        Raises:
            ValidationException: 用户名或邮箱已存在时抛出
        """
        # 检查用户名是否已存在
        user = await crud_user.get_by_username(session, obj_in.username)
        if user:
            raise ValidationException("用户名已存在")

        # 检查邮箱是否已存在
        user = await crud_user.get_by_email(session, obj_in.email)
        if user:
            raise ValidationException("邮箱已存在")

        # 创建用户
        user = await crud_user.create(session, obj_in=obj_in)
        return user

    async def update_user(
            self,
            session: AsyncSession,
            user_id: int,
            obj_in: SysUserUpdate
    ) -> SysUser:
        """
        更新用户
        
        Args:
            session: 数据库会话
            user_id: 用户 ID
            obj_in: 用户更新数据
            
        Returns:
            SysUser: 更新后的用户对象
            
        Raises:
            NotFoundException: 用户不存在时抛出
            ValidationException: 邮箱已存在时抛出
        """
        # 1. 查找是否存在
        db_obj = await crud_user.get(session, user_id)
        if not db_obj:
            raise NotFoundException("用户不存在")

        # 2. 检查邮箱唯一性 (如果修改了邮箱)
        if obj_in.email and obj_in.email != db_obj.email:
            if await crud_user.get_by_email(session, obj_in.email):
                raise ValidationException("邮箱已存在")

        user = await crud_user.update(
            session,
            db_obj=db_obj,
            obj_in=obj_in
        )

        return user

    async def update_last_login(
            self,
            session: AsyncSession,
            user_id: int
    ) -> SysUser:
        """
        更新最后登录时间
        
        Args:
            session: 数据库会话
            user_id: 用户 ID
            
        Returns:
            SysUser: 更新后的用户对象
            
        Raises:
            NotFoundException: 用户不存在时抛出
        """
        user = await crud_user.get(session, user_id)
        if not user:
            raise NotFoundException("用户不存在")

        # 使用带时区的 UTC 时间
        user.last_login_at = datetime.now(timezone.utc)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    async def authenticate_user(
            self,
            session: AsyncSession,
            username: str,
            password: str
    ) -> SysUser:
        """
        验证用户
        
        Args:
            session: 数据库会话
            username: 用户名
            password: 密码
            
        Returns:
            SysUser: 认证成功的用户对象
            
        Raises:
            AuthenticationException: 用户名或密码错误、用户被禁用时抛出
        """
        user = await crud_user.authenticate(session, username, password)
        if not user:
            raise AuthenticationException("用户名或密码错误")

        if not user.is_active:
            raise AuthenticationException("用户已被禁用")

        user.last_login_at = datetime.now(timezone.utc)
        session.add(user)
        await session.commit()
        await session.refresh(user)

        return user

    async def get_user_page(
            self,
            session: AsyncSession,
            page: int,
            size: int,
            current_user: SysUser,
    ) -> PageInfo[SysUserResponse]:
        """
        获取用户分页列表
        
        Args:
            session: 数据库会话
            page: 页码
            size: 每页数量
            current_user: 当前登录用户
            
        Returns:
            PageInfo[SysUserResponse]: 用户分页数据
            
        Raises:
            PermissionException: 非超级管理员访问时抛出
        """
        if not current_user.is_superuser:
            raise PermissionException("权限不足")

        users, total = await crud_user.get_page(
            session,
            page=page,
            page_size=size,
            options=[selectinload(SysUser.roles)]  # type: ignore
        )

        user_responses = []
        for user in users:
            # 过滤掉 ID 为 None 的情况，确保类型安全 (List[int])
            role_ids = [role.id for role in user.roles if role.id is not None]

            # 使用 model_validate 转换
            # (确保 SysUserResponse 允许 extra fields 或者手动构建 dict)
            user_resp = SysUserResponse.model_validate(user)
            user_resp.role_ids = role_ids

            user_responses.append(user_resp)

        # 计算总页数
        pages = (total + size - 1) // size if size > 0 else 0
        
        return PageInfo[SysUserResponse](
            items=user_responses,
            total=total,
            page=page,
            size=size,
            pages=pages
        )


sys_user_service = SysUserService()

