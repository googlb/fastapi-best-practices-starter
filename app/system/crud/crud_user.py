from typing import Optional, List
from sqlmodel import select, col
from sqlmodel.ext.asyncio.session import AsyncSession

from app.system.models import SysUser, SysUserRole
from app.system.schemas.user import SysUserCreate, SysUserUpdate
from app.core.security import hash_password, verify_password
from app.db.crud_base import CRUDBase

class CRUDSysUser(CRUDBase[SysUser, SysUserCreate, SysUserUpdate]):

    async def get_by_username(self, session: AsyncSession, username: str) -> Optional[SysUser]:
        statement = select(SysUser).where(SysUser.username == username)
        result = await session.exec(statement)
        return result.first()

    async def get_by_email(self, session: AsyncSession, email: str) -> Optional[SysUser]:
        statement = select(SysUser).where(SysUser.email == email)
        result = await session.exec(statement)
        return result.first()

    async def create(self, session: AsyncSession, *, obj_in: SysUserCreate) -> SysUser:
        """
        重写 Create：因为需要处理密码哈希，且输入模型(UserCreate)与数据库模型(User)字段不完全一致
        """
        # 1. 转为字典
        create_data = obj_in.model_dump()
        # 2. 弹出明文密码并加密
        password = create_data.pop("password")
        create_data["hashed_password"] = hash_password(password)

        # 3. 创建数据库对象
        db_obj = SysUser.model_validate(create_data)

        # 4. 执行入库
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
        # 这里的实现非常棒，完美利用了 Pydantic 的 exclude_unset
        update_data = obj_in.model_dump(exclude_unset=True)

        if "password" in update_data:
            password = update_data.pop("password")
            update_data["hashed_password"] = hash_password(password)

        return await super().update(session, db_obj=db_obj, obj_in=update_data)

    async def get_by_role_ids(self, session: AsyncSession, role_ids: List[int]) -> List[SysUser]:
        """
        根据角色ID列表获取用户
        修复了之前的逻辑错误，使用 join 查询中间表
        """
        statement = (
            select(SysUser)
            .join(SysUserRole, SysUser.id == SysUserRole.user_id)
            .where(col(SysUserRole.role_id).in_(role_ids))
            .distinct()  # 去重，防止一个用户有多个角色时被查出来多次
        )
        result = await session.exec(statement)
        return result.all()

    async def authenticate(
        self, session: AsyncSession, username: str, password: str
    ) -> Optional[SysUser]:
        user = await self.get_by_username(session, username)
        if not user:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return user

# 实例化
crud_user = CRUDSysUser(SysUser)
