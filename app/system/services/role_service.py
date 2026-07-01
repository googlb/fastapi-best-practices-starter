from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.exceptions import NotFoundException, ValidationException
from app.system.crud.crud_role import crud_role
from app.system.models import SysRole
from app.system.schemas.role import RoleCreate, RoleUpdate


class SysRoleService:
    async def create_role(self, session: AsyncSession, obj_in: RoleCreate) -> SysRole:
        existing = await crud_role.get_by_code(session, obj_in.code)
        if existing:
            raise ValidationException("角色编码已存在")
        return await crud_role.create(session, obj_in=obj_in)

    async def update_role(
        self, session: AsyncSession, role_id: int, obj_in: RoleUpdate
    ) -> SysRole:
        db_obj = await crud_role.get(session, role_id)
        if not db_obj:
            raise NotFoundException("角色不存在")

        if obj_in.code and obj_in.code != db_obj.code:
            existing = await crud_role.get_by_code(session, obj_in.code)
            if existing:
                raise ValidationException("角色编码已存在")

        return await crud_role.update(session, db_obj=db_obj, obj_in=obj_in)

    async def delete_role(self, session: AsyncSession, role_id: int) -> None:
        db_obj = await crud_role.get(session, role_id)
        if not db_obj:
            raise NotFoundException("角色不存在")
        await crud_role.delete(session, id=role_id)


sys_role_service = SysRoleService()
