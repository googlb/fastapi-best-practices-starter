from typing import Optional, List
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.system.models import SysMenu, SysUser, SysRoleMenu
from app.system.schemas.menu import MenuCreate, MenuUpdate, MenuResponse
from app.db.crud_base import CRUDBase



from sqlalchemy.orm import noload

class CRUDMenu(CRUDBase[SysMenu, MenuCreate, MenuUpdate]):

    def _build_pydantic_tree(self, menus: List[MenuResponse]) -> List[MenuResponse]:
        """
        在内存中从 Pydantic 模型列表构建树形结构.
        """
        menus_dict = {menu.id: menu for menu in menus}
        root_menus = []

        for menu in menus:
            if menu.parent_id and menu.parent_id in menus_dict:
                parent_menu = menus_dict[menu.parent_id]
                # The children list in Pydantic model might be None initially
                if parent_menu.children is None:
                    parent_menu.children = []
                parent_menu.children.append(menu)
            else:
                root_menus.append(menu)

        # 为保证前端渲染顺序一致，对子菜单和根菜单进行排序
        for menu in menus:
            if menu.children:
                menu.children.sort(key=lambda m: m.sort)

        root_menus.sort(key=lambda m: m.sort)
        return root_menus

    async def get_tree_by_user(self, session: AsyncSession, user: SysUser) -> List[MenuResponse]:
        """
        通过用户角色获取菜单树.
        """
        # 1. 一次性获取所有菜单, 使用 noload 禁用 children 的懒加载
        all_menus_stmt = select(SysMenu).options(noload(SysMenu.children))
        all_menus_list = (await session.exec(all_menus_stmt)).all()
        all_menus_map = {m.id: m for m in all_menus_list}

        # 2. 获取用户角色允许的所有菜单ID
        role_ids = [role.id for role in user.roles]
        if not role_ids:
            return []
        
        allowed_menu_ids_res = await session.exec(select(SysRoleMenu.menu_id).where(SysRoleMenu.role_id.in_(role_ids)))
        allowed_ids = {i[0] for i in allowed_menu_ids_res}

        # 3. 确定最终菜单集：包含所有允许的菜单及其所有父级
        final_menus_to_include_ids = set()
        for menu in all_menus_list:
            if menu.id in allowed_ids:
                curr = menu
                while curr:
                    final_menus_to_include_ids.add(curr.id)
                    curr = all_menus_map.get(curr.parent_id)
        
        filtered_menu_list_db = [m for m in all_menus_list if m.id in final_menus_to_include_ids]
        
        # 4. 关键步骤：在构建树之前，将DB模型列表转换为Pydantic模型列表
        # 因为查询时用了 noload，这里的 model_validate 不会触发数据库IO
        pydantic_menus = [MenuResponse.model_validate(db_menu) for db_menu in filtered_menu_list_db]

        # 5. 在Pydantic模型列表上构建树并返回
        return self._build_pydantic_tree(pydantic_menus)

    async def get_tree(self, session: AsyncSession, parent_id: Optional[int] = None) -> List[MenuResponse]:
        """获取菜单树形结构 (高效版, 供超级管理员使用)"""
        # 1. 一次性获取所有菜单，使用 noload 禁用 children 的懒加载
        statement = select(SysMenu).options(noload(SysMenu.children)).order_by(SysMenu.sort)
        all_menus_db = (await session.exec(statement)).all()
        
        # 2. 关键步骤：将DB模型转换为Pydantic模型
        # 因为查询时用了 noload，这里的 model_validate 不会触发数据库IO
        all_menus_pydantic = [MenuResponse.model_validate(db_menu) for db_menu in all_menus_db]

        # 3. 在Pydantic模型列表上构建树
        root_menus = self._build_pydantic_tree(all_menus_pydantic)

        # (可选) 支持按 parent_id 查询子树
        if parent_id is not None:
            menus_dict = {menu.id: menu for menu in all_menus_pydantic}
            parent_menu = menus_dict.get(parent_id)
            return parent_menu.children if parent_menu and parent_menu.children else []
        
        return root_menus
    
    async def get_children(self, session: AsyncSession, parent_id: int) -> List[SysMenu]:
        """获取子菜单"""
        statement = select(SysMenu).where(SysMenu.parent_id == parent_id)
        result = await session.exec(statement)
        return result.all()



crud_menu = CRUDMenu(SysMenu)
