from typing import Optional, List
from uuid import UUID
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.system.models import SysDictData
from app.system.schemas.dict import DictDataCreate, DictDataUpdate
from app.db.crud_base import CRUDBase


class CRUDDictData(CRUDBase[SysDictData, DictDataCreate, DictDataUpdate]):
    async def get_by_dict_id(self, session: AsyncSession, dict_id: UUID) -> List[SysDictData]:
        """根据字典ID获取字典数据列表"""
        statement = select(SysDictData).where(SysDictData.dict_id == dict_id)
        result = await session.exec(statement)
        return result.all()


crud_dict_data = CRUDDictData(SysDictData)
