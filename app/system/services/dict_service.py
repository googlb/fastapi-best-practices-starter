from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.exceptions import NotFoundException
from app.system.crud.crud_dict import crud_dict
from app.system.crud.crud_dict_data import crud_dict_data
from app.system.models import SysDict
from app.system.schemas.dict import (
    DictCreate,
    DictDataCreate,
    DictDataUpdate,
    DictUpdate,
)


class SysDictService:
    async def create_dict(self, session: AsyncSession, obj_in: DictCreate) -> SysDict:
        return await crud_dict.create(session, obj_in=obj_in)

    async def update_dict(
        self, session: AsyncSession, dict_id: int, obj_in: DictUpdate
    ) -> SysDict:
        db_obj = await crud_dict.get(session, dict_id)
        if not db_obj:
            raise NotFoundException("字典不存在")
        return await crud_dict.update(session, db_obj=db_obj, obj_in=obj_in)

    async def delete_dict(self, session: AsyncSession, dict_id: int) -> None:
        db_obj = await crud_dict.get(session, dict_id)
        if not db_obj:
            raise NotFoundException("字典不存在")
        await crud_dict.delete(session, id=dict_id)

    async def get_dict_by_code(self, session: AsyncSession, code: str) -> dict | None:
        dict_item = await crud_dict.get_by_code(session, code)
        if not dict_item:
            return None

        dict_data_list = await crud_dict_data.get_by_dict_id(session, dict_item.id)
        return {
            "id": dict_item.id,
            "name": dict_item.name,
            "code": dict_item.code,
            "description": dict_item.description,
            "created_at": dict_item.created_at,
            "updated_at": dict_item.updated_at,
            "data": dict_data_list,
        }

    async def create_dict_data(
        self, session: AsyncSession, dict_id: int, obj_in: DictDataCreate
    ):
        db_obj = await crud_dict.get(session, dict_id)
        if not db_obj:
            raise NotFoundException("字典不存在")
        obj_in.dict_id = dict_id
        return await crud_dict_data.create(session, obj_in=obj_in)

    async def update_dict_data(
        self, session: AsyncSession, data_id: int, obj_in: DictDataUpdate
    ):
        db_obj = await crud_dict_data.get(session, data_id)
        if not db_obj:
            raise NotFoundException("字典数据不存在")
        return await crud_dict_data.update(session, db_obj=db_obj, obj_in=obj_in)

    async def delete_dict_data(self, session: AsyncSession, data_id: int) -> None:
        db_obj = await crud_dict_data.get(session, data_id)
        if not db_obj:
            raise NotFoundException("字典数据不存在")
        await crud_dict_data.delete(session, id=data_id)


sys_dict_service = SysDictService()
