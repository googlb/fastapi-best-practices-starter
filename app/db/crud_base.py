from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union, Tuple, Sequence
from pydantic import BaseModel
from sqlmodel import SQLModel, select, func, col
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, session: AsyncSession, id: Any) -> Optional[ModelType]:
        return await session.get(self.model, id)

    async def get_page(
        self,
        session: AsyncSession,
        *,
        page: int = 1,
        page_size: int = 10,
        options: Optional[Sequence[ExecutableOption]] = None,
        **kwargs: Any
    ) -> Tuple[List[ModelType], int]:
        statement = select(self.model)

        for key, value in kwargs.items():
            if value is not None and hasattr(self.model, key):
                statement = statement.where(getattr(self.model, key) == value)

        count_statement = select(func.count()).select_from(statement.subquery())
        total_result = await session.exec(count_statement)
        total = total_result.one()

        if options:
            for option in options:
                statement = statement.options(option)

        offset = (page - 1) * page_size
        statement = statement.offset(offset).limit(page_size)

        if hasattr(self.model, "created_at"):
            statement = statement.order_by(col(getattr(self.model, "created_at")).desc())

        result = await session.exec(statement)
        return result.all(), total

    async def create(
        self, session: AsyncSession, *, obj_in: CreateSchemaType
    ) -> ModelType:
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
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = db_obj.model_dump()
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def delete(self, session: AsyncSession, *, id: Any) -> bool:
        db_obj = await session.get(self.model, id)
        if not db_obj:
            return False
        await session.delete(db_obj)
        await session.commit()
        return True
