from typing import Optional, List
from uuid import UUID
from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession

from app.business.models import News, Order, Product, ProductCategory
from app.business.schemas.business import (
    NewsCreate, NewsUpdate,
    OrderCreate, OrderUpdate,
    ProductCreate, ProductUpdate,
    ProductCategoryCreate, ProductCategoryUpdate
)


class CRUDNews:
    async def get(self, session: AsyncSession, id: int) -> Optional[News]:
        """获取单个新闻"""
        statement = select(News).where(News.id == id)
        result = await session.exec(statement)
        return result.first()
    
    async def get_multi(
        self, 
        session: AsyncSession, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        author_id: Optional[UUID] = None,
        is_published: Optional[bool] = None
    ) -> List[News]:
        """获取多个新闻"""
        statement = select(News)
        
        if author_id:
            statement = statement.where(News.author_id == author_id)
        
        if is_published is not None:
            statement = statement.where(News.is_published == is_published)
        
        statement = statement.offset(skip).limit(limit).order_by(News.created_at.desc())
        result = await session.exec(statement)
        return result.all()
    
    async def create(self, session: AsyncSession, *, obj_in: NewsCreate, author_id: UUID) -> News:
        """创建新闻"""
        obj_data = obj_in.model_dump()
        db_obj = News.model_validate(obj_data, update={"author_id": author_id})
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def update(
        self, 
        session: AsyncSession, 
        *, 
        db_obj: News, 
        obj_in: NewsUpdate
    ) -> News:
        """更新新闻"""
        obj_data = obj_in.model_dump(exclude_unset=True)
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def delete(self, session: AsyncSession, *, id: int) -> Optional[News]:
        """删除新闻"""
        obj = await self.get(session, id)
        if obj:
            await session.delete(obj)
            await session.commit()
        return obj


class CRUDOrder:
    async def get(self, session: AsyncSession, id: int) -> Optional[Order]:
        """获取单个订单"""
        statement = select(Order).where(Order.id == id)
        result = await session.exec(statement)
        return result.first()
    
    async def get_by_order_no(self, session: AsyncSession, order_no: str) -> Optional[Order]:
        """根据订单号获取订单"""
        statement = select(Order).where(Order.order_no == order_no)
        result = await session.exec(statement)
        return result.first()
    
    async def get_multi(
        self, 
        session: AsyncSession, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        customer_id: Optional[UUID] = None,
        status: Optional[str] = None
    ) -> List[Order]:
        """获取多个订单"""
        statement = select(Order)
        
        if customer_id:
            statement = statement.where(Order.customer_id == customer_id)
        
        if status:
            statement = statement.where(Order.status == status)
        
        statement = statement.offset(skip).limit(limit).order_by(Order.created_at.desc())
        result = await session.exec(statement)
        return result.all()
    
    async def create(self, session: AsyncSession, *, obj_in: OrderCreate, customer_id: UUID) -> Order:
        """创建订单"""
        obj_data = obj_in.model_dump()
        db_obj = Order.model_validate(obj_data, update={"customer_id": customer_id})
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def update(
        self, 
        session: AsyncSession, 
        *, 
        db_obj: Order, 
        obj_in: OrderUpdate
    ) -> Order:
        """更新订单"""
        obj_data = obj_in.model_dump(exclude_unset=True)
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def delete(self, session: AsyncSession, *, id: int) -> Optional[Order]:
        """删除订单"""
        obj = await self.get(session, id)
        if obj:
            await session.delete(obj)
            await session.commit()
        return obj


class CRUDProduct:
    async def get(self, session: AsyncSession, id: int) -> Optional[Product]:
        """获取单个产品"""
        statement = select(Product).where(Product.id == id)
        result = await session.exec(statement)
        return result.first()
    
    async def get_multi(
        self, 
        session: AsyncSession, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        category_id: Optional[int] = None,
        is_active: Optional[bool] = None
    ) -> List[Product]:
        """获取多个产品"""
        statement = select(Product)
        
        if category_id:
            statement = statement.where(Product.category_id == category_id)
        
        if is_active is not None:
            statement = statement.where(Product.is_active == is_active)
        
        statement = statement.offset(skip).limit(limit).order_by(Product.created_at.desc())
        result = await session.exec(statement)
        return result.all()
    
    async def create(self, session: AsyncSession, *, obj_in: ProductCreate) -> Product:
        """创建产品"""
        obj_data = obj_in.model_dump()
        db_obj = Product.model_validate(obj_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def update(
        self, 
        session: AsyncSession, 
        *, 
        db_obj: Product, 
        obj_in: ProductUpdate
    ) -> Product:
        """更新产品"""
        obj_data = obj_in.model_dump(exclude_unset=True)
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def delete(self, session: AsyncSession, *, id: int) -> Optional[Product]:
        """删除产品"""
        obj = await self.get(session, id)
        if obj:
            await session.delete(obj)
            await session.commit()
        return obj


class CRUDProductCategory:
    async def get(self, session: AsyncSession, id: int) -> Optional[ProductCategory]:
        """获取单个产品分类"""
        statement = select(ProductCategory).where(ProductCategory.id == id)
        result = await session.exec(statement)
        return result.first()
    
    async def get_multi(
        self, 
        session: AsyncSession, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        parent_id: Optional[int] = None,
        is_active: Optional[bool] = None
    ) -> List[ProductCategory]:
        """获取多个产品分类"""
        statement = select(ProductCategory)
        
        if parent_id is not None:
            statement = statement.where(ProductCategory.parent_id == parent_id)
        
        if is_active is not None:
            statement = statement.where(ProductCategory.is_active == is_active)
        
        statement = statement.offset(skip).limit(limit).order_by(ProductCategory.sort_order, ProductCategory.name)
        result = await session.exec(statement)
        return result.all()
    
    async def get_tree(self, session: AsyncSession) -> List[ProductCategory]:
        """获取分类树"""
        # 获取所有一级分类
        statement = select(ProductCategory).where(ProductCategory.parent_id.is_(None))
        result = await session.exec(statement)
        categories = result.all()
        
        # 为每个分类加载子分类
        for category in categories:
            await self._load_children(session, category)
        
        return categories
    
    async def _load_children(self, session: AsyncSession, category: ProductCategory):
        """递归加载子分类"""
        statement = select(ProductCategory).where(ProductCategory.parent_id == category.id)
        result = await session.exec(statement)
        children = result.all()
        
        if children:
            category.children = children
            for child in children:
                await self._load_children(session, child)
    
    async def create(self, session: AsyncSession, *, obj_in: ProductCategoryCreate) -> ProductCategory:
        """创建产品分类"""
        obj_data = obj_in.model_dump()
        db_obj = ProductCategory.model_validate(obj_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def update(
        self, 
        session: AsyncSession, 
        *, 
        db_obj: ProductCategory, 
        obj_in: ProductCategoryUpdate
    ) -> ProductCategory:
        """更新产品分类"""
        obj_data = obj_in.model_dump(exclude_unset=True)
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def delete(self, session: AsyncSession, *, id: int) -> Optional[ProductCategory]:
        """删除产品分类"""
        obj = await self.get(session, id)
        if obj:
            await session.delete(obj)
            await session.commit()
        return obj


# 创建CRUD实例
crud_news = CRUDNews()
crud_order = CRUDOrder()
crud_product = CRUDProduct()
crud_product_category = CRUDProductCategory()
