from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from uuid import UUID
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlmodel import SQLModel, select, and_
from sqlmodel.ext.asyncio.session import AsyncSession

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLModel model class
        """
        self.model = model

    async def get(self, session: AsyncSession, id: Any) -> Optional[ModelType]:
        """
        获取单个记录
        """
        statement = select(self.model).where(self.model.id == id)
        result = await session.exec(statement)
        return result.first()

    async def get_multi(
        self, session: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """
        获取多个记录（分页）
        """
        statement = select(self.model).offset(skip).limit(limit)
        result = await session.exec(statement)
        return result.all()

    async def get_multi_by(
        self, session: AsyncSession, *, skip: int = 0, limit: int = 100, **kwargs
    ) -> List[ModelType]:
        """
        根据条件获取多个记录（分页）
        """
        conditions = []
        for key, value in kwargs.items():
            if hasattr(self.model, key):
                conditions.append(getattr(self.model, key) == value)

        if conditions:
            statement = select(self.model).where(and_(*conditions)).offset(skip).limit(limit)
        else:
            statement = select(self.model).offset(skip).limit(limit)

        result = await session.exec(statement)
        return result.all()

    async def create(
        self, session: AsyncSession, *, obj_in: CreateSchemaType
    ) -> ModelType:
        """
        创建新记录
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
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
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(self, session: AsyncSession, *, id: Any) -> Optional[ModelType]:
        """
        删除记录
        """
        obj = await self.get(session, id)
        if obj:
            await session.delete(obj)
            await session.commit()
        return obj

    async def count(self, session: AsyncSession) -> int:
        """
        获取记录总数
        """
        statement = select(self.model)
        result = await session.exec(statement)
        return len(result.all())
