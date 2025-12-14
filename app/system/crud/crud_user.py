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
        # 转换为字典并处理密码
        obj_in_data = obj_in.model_dump()
        obj_in_data["hashed_password"] = hash_password(obj_in_data.pop("password"))
        
        # 使用基类的model_validate方法创建对象
        db_obj = self.model.model_validate(obj_in_data)
        
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
        # 获取更新数据
        update_data = obj_in.model_dump(exclude_unset=True)
        
        # 处理密码
        if "password" in update_data:
            update_data["hashed_password"] = hash_password(update_data.pop("password"))
        
        # 使用基类的update方法
        return await super().update(session, db_obj=db_obj, obj_in=update_data)

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
