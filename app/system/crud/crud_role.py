from typing import Optional, List
from uuid import UUID
from sqlmodel import Session, select, and_
from sqlmodel.ext.asyncio.session import AsyncSession
from app.system.models import SysRole
from app.db.crud_base import CRUDBase


class CRUDRole(CRUDBase[SysRole]):
    async def get(self, session: AsyncSession, id: UUID) -> Optional[SysRole]:
        """根据ID获取角色"""
        statement = select(SysRole).where(SysRole.id == id)
        result = await session.execute(statement)
        return result.scalar_one_or_none()
    
    async def get_by_code(self, session: AsyncSession, code: str) -> Optional[SysRole]:
        """根据编码获取角色"""
        statement = select(SysRole).where(SysRole.code == code)
        result = await session.execute(statement)
        return result.scalar_one_or_none()
    
    async def get_multi(self, session: AsyncSession, skip: int = 0, limit: int = 100) -> List[SysRole]:
        """获取角色列表"""
        statement = select(SysRole).offset(skip).limit(limit)
        result = await session.execute(statement)
        return result.scalars().all()
    
    async def create(self, session: AsyncSession, obj_in: dict) -> SysRole:
        """创建角色"""
        db_obj = SysRole(**obj_in)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def update(self, session: AsyncSession, db_obj: SysRole, obj_in: dict) -> SysRole:
        """更新角色"""
        for key, value in obj_in.items():
            setattr(db_obj, key, value)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def delete(self, session: AsyncSession, id: UUID) -> Optional[SysRole]:
        """删除角色"""
        obj = await self.get(session, id)
        if obj:
            await session.delete(obj)
            await session.commit()
        return obj
    
    async def get_with_menus(self, session: AsyncSession, id: UUID) -> Optional[SysRole]:
        """获取角色及其关联的菜单"""
        role = await self.get(session, id)
        if role:
            from app.system.crud.crud_role_menu import crud_role_menu
            role_menus = await crud_role_menu.get_role_menus(session, id)
            role.menus = role_menus
        return role


crud_role = CRUDRole()
