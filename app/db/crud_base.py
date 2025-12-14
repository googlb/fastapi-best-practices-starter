from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union, Tuple
from pydantic import BaseModel
from sqlmodel import SQLModel, select, func, col
from sqlmodel.ext.asyncio.session import AsyncSession

# 定义泛型变量
ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD 基础类，封装了基础的增删改查方法
        :param model: SQLModel 模型类
        """
        self.model = model

    async def get(self, session: AsyncSession, id: Any) -> Optional[ModelType]:
        """
        通过主键获取单条记录
        """
        # SQLModel 的 session.get 针对主键查询有优化
        return await session.get(self.model, id)

    async def get_page(
        self,
        session: AsyncSession,
        *,
        page: int = 1,
        page_size: int = 10,
        **kwargs
    ) -> Tuple[List[ModelType], int]:
        """
        获取分页列表 (包含总数)
        :return: (items, total_count)
        """
        # 1. 构建基础查询
        statement = select(self.model)

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
        return result.all(), total

    async def create(
        self, session: AsyncSession, *, obj_in: CreateSchemaType
    ) -> ModelType:
        """
        创建记录
        """
        # Pydantic v2 推荐写法: model_dump()
        obj_in_data = obj_in.model_dump()

        # 使用 model_validate 替代直接解包，更加安全
        db_obj = self.model.model_validate(obj_in_data)

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        session: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        更新记录
        """
        # 1. 获取现有数据的字典格式
        obj_data = db_obj.model_dump()

        # 2. 获取更新数据的字典格式
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            # exclude_unset=True 确保只更新前端传过来的字段
            update_data = obj_in.model_dump(exclude_unset=True)

        # 3. 智能赋值
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def delete(self, session: AsyncSession, *, id: Any) -> bool:
        """
        删除记录 (物理删除)
        """
        db_obj = await session.get(self.model, id)
        if not db_obj:
            return False

        await session.delete(db_obj)
        await session.commit()
        return True

    # 如果有软删除需求，可以增加这个方法
    async def soft_delete(self, session: AsyncSession, *, id: Any) -> bool:
        """
        软删除 (需要 Model 有 is_deleted 字段)
        """
        db_obj = await session.get(self.model, id)
        if not db_obj:
            return False

        if hasattr(db_obj, "is_deleted"):
            db_obj.is_deleted = True # type: ignore
            session.add(db_obj)
            await session.commit()
            return True
        return False
