from typing import Optional, List, Tuple, Any
from sqlmodel import select, func, col
from sqlmodel.ext.asyncio.session import AsyncSession
from app.system.models import SysDictData
from app.system.schemas.dict import DictDataCreate, DictDataUpdate
from app.db.crud_base import CRUDBase


class CRUDDictData(CRUDBase[SysDictData, DictDataCreate, DictDataUpdate]):
    async def get_by_dict_id(self, session: AsyncSession, dict_id: int, skip: int = 0, limit: int = 100) -> List[SysDictData]:
        """根据字典ID获取字典数据列表"""
        statement = select(SysDictData).where(SysDictData.dict_id == dict_id).offset(skip).limit(limit)
        result = await session.exec(statement)
        return list(result.all())
    
    async def count_by_dict_id(self, session: AsyncSession, dict_id: int) -> int:
        """根据字典ID获取字典数据总数"""
        statement = select(func.count()).select_from(SysDictData).where(SysDictData.dict_id == dict_id)
        result = await session.exec(statement)
        return result.one()
    
    async def get_page(
        self,
        session: AsyncSession,
        *,
        page: int = 1,
        page_size: int = 10,
        dict_id: Optional[int] = None,
        **kwargs: Any
    ) -> Tuple[List[SysDictData], int]:
        """
        获取分页列表 (包含总数)
        :return: (items, total_count)
        """
        # 1. 构建基础查询
        statement = select(self.model)
        
        # 添加字典ID过滤条件
        if dict_id is not None:
            statement = statement.where(self.model.dict_id == dict_id)

        # 2. 动态添加过滤条件 (简单的相等查询)
        for key, value in kwargs.items():
            if value is not None and hasattr(self.model, key):
                statement = statement.where(getattr(self.model, key) == value)

        # 3. 计算总数 (性能优化：只查询 ID 或使用 count(*))
        # 使用 func.count() 避免加载所有数据到内存
        count_statement = select(func.count()).select_from(statement.subquery())
        total_result = await session.exec(count_statement)
        total = total_result.one()

        # 4. 分页查询
        # 注意：前端通常传 page/page_size，数据库需要 offset/limit
        offset = (page - 1) * page_size
        statement = statement.offset(offset).limit(page_size)

        # 可选：默认按创建时间倒序 (如果表里有 created_at)
        if hasattr(self.model, "created_at"):
             # type: ignore
            statement = statement.order_by(col(getattr(self.model, "created_at")).desc())

        result = await session.exec(statement)
        return list(result.all()), total


crud_dict_data = CRUDDictData(SysDictData)
