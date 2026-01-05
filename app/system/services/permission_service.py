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
        """
        statement = (
            select(SysMenu.permission)
            .join(SysRoleMenu, SysRoleMenu.menu_id == SysMenu.id)
            .join(SysUserRole, SysUserRole.role_id == SysRoleMenu.role_id)
            .where(SysUserRole.user_id == user_id)
            .where(SysMenu.status == 1) # 菜单必须是启用状态
            .where(SysMenu.permission != None) # 过滤掉没有权限标识的目录
            .where(SysMenu.permission != "")
            .distinct()
        )

        result = await session.exec(statement)
        return list(result.all())

permission_service = PermissionService()
