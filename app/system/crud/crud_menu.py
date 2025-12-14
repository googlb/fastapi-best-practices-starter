from typing import Optional, List
from uuid import UUID
from sqlmodel import Session, select, and_
from sqlmodel.ext.asyncio.session import AsyncSession
from app.system.models import SysMenu
from app.db.crud_base import CRUDBase


class CRUDMenu(CRUDBase[SysMenu]):
    async def get(self, session: AsyncSession, id: UUID) -> Optional[SysMenu]:
        """根据ID获取菜单"""
        statement = select(SysMenu).where(SysMenu.id == id)
        result = await session.execute(statement)
        return result.scalar_one_or_none()
    
    async def get_multi(self, session: AsyncSession, skip: int = 0, limit: int = 100) -> List[SysMenu]:
        """获取菜单列表"""
        statement = select(SysMenu).offset(skip).limit(limit)
        result = await session.execute(statement)
        return result.scalars().all()
    
    async def get_tree(self, session: AsyncSession, parent_id: Optional[UUID] = None) -> List[SysMenu]:
        """获取菜单树形结构"""
        statement = select(SysMenu).where(SysMenu.parent_id == parent_id)
        result = await session.execute(statement)
        menus = result.scalars().all()
        
        # 递归获取子菜单
        for menu in menus:
            menu.children = await self.get_tree(session, menu.id)
        
        return menus
    
    async def get_children(self, session: AsyncSession, parent_id: UUID) -> List[SysMenu]:
        """获取子菜单"""
        statement = select(SysMenu).where(SysMenu.parent_id == parent_id)
        result = await session.execute(statement)
        return result.scalars().all()
    
    async def create(self, session: AsyncSession, obj_in: dict) -> SysMenu:
        """创建菜单"""
        db_obj = SysMenu(**obj_in)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def update(self, session: AsyncSession, db_obj: SysMenu, obj_in: dict) -> SysMenu:
        """更新菜单"""
        for key, value in obj_in.items():
            setattr(db_obj, key, value)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def delete(self, session: AsyncSession, id: UUID) -> Optional[SysMenu]:
        """删除菜单"""
        obj = await self.get(session, id)
        if obj:
            await session.delete(obj)
            await session.commit()
        return obj


crud_menu = CRUDMenu()
