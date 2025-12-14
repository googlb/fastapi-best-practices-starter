from typing import Optional, List
from uuid import UUID
from sqlmodel import select, and_
from sqlmodel.ext.asyncio.session import AsyncSession
from app.system.models import SysRole
from app.system.schemas.role import RoleCreate, RoleUpdate
from app.db.crud_base import CRUDBase


class CRUDRole(CRUDBase[SysRole, RoleCreate, RoleUpdate]):
    async def get_by_code(self, session: AsyncSession, code: str) -> Optional[SysRole]:
        """根据编码获取角色"""
        statement = select(SysRole).where(SysRole.code == code)
        result = await session.exec(statement)
        return result.first()
    
    async def get_with_menus(self, session: AsyncSession, id: UUID) -> Optional[SysRole]:
        """获取角色及其关联的菜单"""
        role = await self.get(session, id)
        if role:
            from app.system.crud.crud_role_menu import crud_role_menu
            role_menus = await crud_role_menu.get_role_menus(session, id)
            role.menus = role_menus
        return role


crud_role = CRUDRole(SysRole)
