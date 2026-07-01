from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.exceptions import NotFoundException
from app.system.crud.crud_menu import crud_menu
from app.system.crud.crud_role_menu import crud_role_menu
from app.system.models import SysMenu, SysUser
from app.system.schemas.menu import MenuCreate, MenuResponse, MenuUpdate


class SysMenuService:
    async def get_user_menu_tree(
        self, session: AsyncSession, user: SysUser
    ) -> list[MenuResponse]:
        if user.is_superuser:
            return await crud_menu.get_tree(session)
        return await crud_menu.get_tree_by_user(session, user)

    async def create_menu(self, session: AsyncSession, obj_in: MenuCreate) -> SysMenu:
        return await crud_menu.create(session, obj_in=obj_in)

    async def update_menu(
        self, session: AsyncSession, menu_id: int, obj_in: MenuUpdate
    ) -> SysMenu:
        db_obj = await crud_menu.get(session, menu_id)
        if not db_obj:
            raise NotFoundException("菜单不存在")
        return await crud_menu.update(session, db_obj=db_obj, obj_in=obj_in)

    async def delete_menu(self, session: AsyncSession, menu_id: int) -> None:
        db_obj = await crud_menu.get(session, menu_id)
        if not db_obj:
            raise NotFoundException("菜单不存在")
        await crud_menu.delete(session, id=menu_id)

    async def get_menu_roles(self, session: AsyncSession, menu_id: int) -> list:
        db_obj = await crud_menu.get(session, menu_id)
        if not db_obj:
            raise NotFoundException("菜单不存在")
        return await crud_role_menu.get_menu_roles(session, menu_id)


sys_menu_service = SysMenuService()
