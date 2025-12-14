from typing import Optional, List
from uuid import UUID
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.system.models import SysDict
from app.system.schemas.dict import DictCreate, DictUpdate
from app.db.crud_base import CRUDBase


class CRUDDict(CRUDBase[SysDict, DictCreate, DictUpdate]):
    async def get_by_code(self, session: AsyncSession, code: str) -> Optional[SysDict]:
        """根据编码获取字典"""
        statement = select(SysDict).where(SysDict.code == code)
        result = await session.exec(statement)
        return result.first()


crud_dict = CRUDDict(SysDict)
