from typing import Any, Generic, TypeVar, Sequence
from pydantic import BaseModel
from sqlmodel import SQLModel, select, func, col
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        """
        self.model = model

    async def get(self, session: AsyncSession, id: Any) -> ModelType | None:
        """
        通过主键获取单个对象
        """
        return await session.get(self.model, id)

    async def get_page(
        self,
        session: AsyncSession,
        *,
        page: int = 1,
        page_size: int = 10,
        # 允许传入复杂的过滤条件，不仅仅是相等
        filters: Sequence[Any] | None = None,
        # 允许传入自定义排序，例如 [col(User.created_at).desc()]
        order_by: Sequence[Any] | None = None,
        # 允许传入 eager loading 选项，如 selectinload
        options: Sequence[ExecutableOption] | None = None,
        # 简单的相等过滤依然可以通过 kwargs 传入
        **kwargs: Any
    ) -> tuple[list[ModelType], int]:
        """
        分页查询，支持复杂过滤、排序和选项
        """
        statement = select(self.model)

        # 1. 处理 kwargs (简单相等查询)
        for key, value in kwargs.items():
            # 只有当 value 不为 None 且模型有该字段时才过滤
            if value is not None and hasattr(self.model, key):
                statement = statement.where(getattr(self.model, key) == value)

        # 2. 处理复杂 filters (如 >, <, like 等)
        if filters:
            for criterion in filters:
                statement = statement.where(criterion)

        # 3. 计算总数 (这是分页中最耗时的部分)
        # 最佳实践：使用 subquery 是为了确保 where 条件生效，
        # 如果追求极致性能且无 join，可优化为 select(func.count()).select_from(self.model).where(...)
        count_statement = select(func.count()).select_from(statement.subquery())
        total_result = await session.exec(count_statement)
        total = total_result.one()

        # 4. 应用 ORM 选项 (如 joinedload)
        if options:
            for option in options:
                statement = statement.options(option)

        # 5. 处理排序
        if order_by:
            for order in order_by:
                statement = statement.order_by(order)
        elif hasattr(self.model, "created_at"):
            # 默认回退策略
            statement = statement.order_by(col(getattr(self.model, "created_at")).desc())

        # 6. 分页切片
        offset = (page - 1) * page_size
        statement = statement.offset(offset).limit(page_size)

        result = await session.exec(statement)
        return list(result.all()), total

    async def create(
        self, session: AsyncSession, *, obj_in: CreateSchemaType
    ) -> ModelType:
        """
        创建新对象
        """
        obj_in_data = obj_in.model_dump()
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
        obj_in: UpdateSchemaType | dict[str, Any]
    ) -> ModelType:
        """
        更新对象
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            # exclude_unset=True 是关键，防止将未传字段更新为 None
            update_data = obj_in.model_dump(exclude_unset=True)

        # 最佳实践：使用 sqlmodel_update 方法 (SQLModel 0.0.14+)
        # 这比手动 setattr 更健壮，且能处理 SQLModel 的内部逻辑
        db_obj.sqlmodel_update(update_data)

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def delete(self, session: AsyncSession, *, id: Any) -> bool:
        """
        删除对象
        """
        db_obj = await session.get(self.model, id)
        if not db_obj:
            return False
        await session.delete(db_obj)
        await session.commit()
        return True
