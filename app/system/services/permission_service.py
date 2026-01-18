# app/system/services/permission_service.py
from typing import List
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.system.models import SysUser, SysUserRole, SysRoleMenu, SysMenu


class PermissionService:
    async def get_user_permissions(self, session: AsyncSession, user_id: int) -> List[str]:
        """
        获取用户的所有权限标识 (去重)
        
        SQL逻辑: User -> UserRole -> Role -> RoleMenu -> Menu
        
        Args:
            session: 数据库会话
            user_id: 用户 ID
            
        Returns:
            List[str]: 用户的权限标识列表（已去重）
        """
        statement = (
            select(SysMenu.permission)
            .join(SysRoleMenu, SysRoleMenu.menu_id == SysMenu.id)
            .join(SysUserRole, SysUserRole.role_id == SysRoleMenu.role_id)
            .where(SysUserRole.user_id == user_id)
            .where(SysMenu.status == 1)  # 菜单必须是启用状态
            .where(SysMenu.permission != None)
            .where(SysMenu.permission != "")
            .distinct()
        )

        result = await session.exec(statement)
        # 过滤掉 None 值，确保返回 List[str]
        permissions = [p for p in result.all() if p is not None]
        return permissions


permission_service = PermissionService()

