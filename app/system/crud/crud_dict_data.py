from typing import Optional, List, Tuple
from uuid import UUID
from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession
from app.system.models import SysDictData
from app.system.schemas.dict import DictDataCreate, DictDataUpdate
from app.db.crud_base import CRUDBase


class CRUDDictData(CRUDBase[SysDictData, DictDataCreate, DictDataUpdate]):
    async def get_by_dict_id(self, session: AsyncSession, dict_id: UUID, skip: int = 0, limit: int = 100) -> List[SysDictData]:
        """根据字典ID获取字典数据列表"""
        statement = select(SysDictData).where(SysDictData.dict_id == dict_id).offset(skip).limit(limit)
        result = await session.exec(statement)
        return result.all()
    
    async def count_by_dict_id(self, session: AsyncSession, dict_id: UUID) -> int:
        """根据字典ID获取字典数据总数"""
        statement = select(func.count()).select_from(SysDictData).where(SysDictData.dict_id == dict_id)
        result = await session.exec(statement)
        return result.one()


crud_dict_data = CRUDDictData(SysDictData)
