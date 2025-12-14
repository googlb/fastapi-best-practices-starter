from typing import Optional, List
from uuid import UUID
from sqlmodel import select, and_
from sqlmodel.ext.asyncio.session import AsyncSession
from app.system.models import SysMenu
from app.system.schemas.menu import MenuCreate, MenuUpdate
from app.db.crud_base import CRUDBase


class CRUDMenu(CRUDBase[SysMenu, MenuCreate, MenuUpdate]):
    async def get_tree(self, session: AsyncSession, parent_id: Optional[UUID] = None) -> List[SysMenu]:
        """获取菜单树形结构"""
        statement = select(SysMenu).where(SysMenu.parent_id == parent_id)
        result = await session.exec(statement)
        menus = result.all()
        
        # 递归获取子菜单
        for menu in menus:
            menu.children = await self.get_tree(session, menu.id)
        
        return menus
    
    async def get_children(self, session: AsyncSession, parent_id: UUID) -> List[SysMenu]:
        """获取子菜单"""
        statement = select(SysMenu).where(SysMenu.parent_id == parent_id)
        result = await session.exec(statement)
        return result.all()


crud_menu = CRUDMenu(SysMenu)
