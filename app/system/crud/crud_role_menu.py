from sqlmodel import select, delete
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List, Optional

from app.system.models import SysRole, SysMenu, SysRoleMenu


class CRUDRoleMenu:
    async def get_role_menus(self, session: AsyncSession, role_id: int) -> List[SysMenu]:
        """获取角色拥有的菜单列表"""
        statement = (
            select(SysMenu)
            .join(SysRoleMenu)
            .where(SysRoleMenu.role_id == role_id)
        )
        result = await session.exec(statement)
        return result.all()
    
    async def get_menu_roles(self, session: AsyncSession, menu_id: int) -> List[SysRole]:
        """获取菜单所属的角色列表"""
        statement = (
            select(SysRole)
            .join(SysRoleMenu)
            .where(SysRoleMenu.menu_id == menu_id)
        )
        result = await session.exec(statement)
        return result.all()
    
    async def assign_menu_to_role(
        self, 
        session: AsyncSession, 
        role_id: int, 
        menu_ids: List[int]
    ) -> bool:
        """为角色分配菜单"""
        try:
            # 先删除该角色的所有菜单关联
            delete_statement = delete(SysRoleMenu).where(SysRoleMenu.role_id == role_id)
            await session.exec(delete_statement)
            
            # 添加新的菜单关联
            for menu_id in menu_ids:
                role_menu = SysRoleMenu(role_id=role_id, menu_id=menu_id)
                session.add(role_menu)
            
            await session.commit()
            return True
        except Exception:
            await session.rollback()
            return False
    
    async def add_menu_to_role(
        self, 
        session: AsyncSession, 
        role_id: int, 
        menu_id: int
    ) -> bool:
        """为角色添加单个菜单"""
        try:
            # 检查是否已存在关联
            statement = select(SysRoleMenu).where(
                SysRoleMenu.role_id == role_id,
                SysRoleMenu.menu_id == menu_id
            )
            result = await session.exec(statement)
            existing = result.scalar_one_or_none()
            
            if existing:
                return True  # 已存在关联
            
            # 创建新关联
            role_menu = SysRoleMenu(role_id=role_id, menu_id=menu_id)
            session.add(role_menu)
            await session.commit()
            return True
        except Exception:
            await session.rollback()
            return False
    
    async def delete_menu_from_role(
        self, 
        session: AsyncSession, 
        role_id: int, 
        menu_id: int
    ) -> bool:
        """从角色中移除菜单"""
        try:
            statement = delete(SysRoleMenu).where(
                SysRoleMenu.role_id == role_id,
                SysRoleMenu.menu_id == menu_id
            )
            await session.exec(statement)
            await session.commit()
            return True
        except Exception:
            await session.rollback()
            return False
    
    async def check_role_has_menu(
        self, 
        session: AsyncSession, 
        role_id: int, 
        menu_id: int
    ) -> bool:
        """检查角色是否拥有指定菜单"""
        statement = select(SysRoleMenu).where(
            SysRoleMenu.role_id == role_id,
            SysRoleMenu.menu_id == menu_id
        )
        result = await session.exec(statement)
        return result.scalar_one_or_none() is not None


crud_role_menu = CRUDRoleMenu()
