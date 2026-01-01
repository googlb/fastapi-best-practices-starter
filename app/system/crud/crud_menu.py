from typing import Optional, List
from sqlmodel import select, and_
from sqlmodel.ext.asyncio.session import AsyncSession
from app.system.models import SysMenu, SysUser, SysRoleMenu
from app.system.schemas.menu import MenuCreate, MenuUpdate
from app.db.crud_base import CRUDBase


class CRUDMenu(CRUDBase[SysMenu, MenuCreate, MenuUpdate]):
    
    def _build_tree_from_flat_list(self, menus: List[SysMenu]) -> List[SysMenu]:
        """
        在内存中从扁平列表构建树形结构.
        """
        menus_dict = {menu.id: menu for menu in menus}
        
        # 重置所有菜单的children列表，避免脏数据
        for menu in menus:
            menu.children = []

        root_menus = []
        for menu in menus:
            if menu.parent_id and menu.parent_id in menus_dict:
                parent_menu = menus_dict[menu.parent_id]
                parent_menu.children.append(menu)
            elif not menu.parent_id:
                root_menus.append(menu)

        # 为保证前端渲染顺序一致，对子菜单和根菜单进行排序
        for menu in menus:
            if menu.children:
                menu.children.sort(key=lambda m: m.sort)
                
        root_menus.sort(key=lambda m: m.sort)
        return root_menus

    async def get_tree_by_user(self, session: AsyncSession, user: SysUser) -> List[SysMenu]:
        """
        通过用户角色获取菜单树.
        1. 获取所有菜单项.
        2. 获取用户角色允许的所有菜单ID.
        3. 确定最终要在树中显示的菜单(所有允许的菜单及其所有父级).
        4. 在内存中构建树.
        """
        # 1. 一次性获取所有菜单
        all_menus_stmt = select(SysMenu)
        all_menus_list = (await session.exec(all_menus_stmt)).all()
        all_menus_map = {m.id: m for m in all_menus_list}

        # 2. 获取用户角色允许的所有菜单ID
        role_ids = [role.id for role in user.roles]
        if not role_ids:
            return []
        
        allowed_menu_ids_res = await session.exec(select(SysRoleMenu.menu_id).where(SysRoleMenu.role_id.in_(role_ids)))
        # 使用集合以提高查找效率
        allowed_ids = {i[0] for i in allowed_menu_ids_res}

        # 3. 确定最终菜单集：包含所有允许的菜单及其所有父级
        final_menus_to_include_ids = set()
        for menu in all_menus_list:
            if menu.id in allowed_ids:
                # 如果一个菜单被允许，那么它和它的所有祖先都应该被包含
                curr = menu
                while curr:
                    final_menus_to_include_ids.add(curr.id)
                    curr = all_menus_map.get(curr.parent_id)
        
        filtered_menu_list = [m for m in all_menus_list if m.id in final_menus_to_include_ids]
        
        # 4. 在内存中构建并返回树
        return self._build_tree_from_flat_list(filtered_menu_list)

    async def get_tree(self, session: AsyncSession, parent_id: Optional[int] = None) -> List[SysMenu]:
        """获取菜单树形结构"""
        statement = select(SysMenu).where(SysMenu.parent_id == parent_id).order_by(SysMenu.sort)
        result = await session.exec(statement)
        menus = result.all()
        
        # 递归获取子菜单
        for menu in menus:
            menu.children = await self.get_tree(session, menu.id)
        
        return menus
    
    async def get_children(self, session: AsyncSession, parent_id: int) -> List[SysMenu]:
        """获取子菜单"""
        statement = select(SysMenu).where(SysMenu.parent_id == parent_id)
        result = await session.exec(statement)
        return result.all()


crud_menu = CRUDMenu(SysMenu)
