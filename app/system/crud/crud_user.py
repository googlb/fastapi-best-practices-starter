from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Optional

from app.system.models import SysUser
from app.system.schemas.user import SysUserCreate, SysUserUpdate
from app.core.security import hash_password, verify_password
from app.db.crud_base import CRUDBase


class CRUDSysUser(CRUDBase[SysUser, SysUserCreate, SysUserUpdate]):
    async def get_by_username(self, session: AsyncSession, username: str) -> Optional[SysUser]:
        """根据用户名获取用户"""
        statement = select(SysUser).where(SysUser.username == username)
        result = await session.exec(statement)
        return result.first()

    async def get_by_email(self, session: AsyncSession, email: str) -> Optional[SysUser]:
        """根据邮箱获取用户"""
        statement = select(SysUser).where(SysUser.email == email)
        result = await session.exec(statement)
        return result.first()

    async def create(self, session: AsyncSession, *, obj_in: SysUserCreate) -> SysUser:
        """创建用户"""
        db_obj = SysUser(
            username=obj_in.username,
            email=obj_in.email,
            hashed_password=hash_password(obj_in.password),
            is_active=obj_in.is_active,
            is_superuser=obj_in.is_superuser,
            remark=obj_in.remark,
            role_id=obj_in.role_id,
        )
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        session: AsyncSession,
        *,
        db_obj: SysUser,
        obj_in: SysUserUpdate
    ) -> SysUser:
        """更新用户"""
        update_data = obj_in.model_dump(exclude_unset=True)

        if "password" in update_data:
            update_data["hashed_password"] = hash_password(update_data.pop("password"))

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def authenticate(
        self, session: AsyncSession, username: str, password: str
    ) -> Optional[SysUser]:
        """验证用户"""
        user = await self.get_by_username(session, username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user


crud_sys_user = CRUDSysUser(SysUser)
