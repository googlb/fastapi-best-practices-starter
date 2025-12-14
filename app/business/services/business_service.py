from typing import Dict, Any, List, Optional
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession

from app.business.crud.crud_business import (
    crud_news, 
    crud_order, 
    crud_product, 
    crud_product_category
)
from app.business.schemas.business import (
    NewsCreate, NewsUpdate,
    OrderCreate, OrderUpdate,
    ProductCreate, ProductUpdate,
    ProductCategoryCreate, ProductCategoryUpdate
)
from app.business.models import News, Order, Product, ProductCategory


class NewsService:
    """新闻服务类"""
    
    async def create_news(
        self, 
        session: AsyncSession, 
        *, 
        obj_in: NewsCreate, 
        author_id: UUID
    ) -> Dict[str, Any]:
        """创建新闻"""
        try:
            news = await crud_news.create(session, obj_in=obj_in, author_id=author_id)
            return {"success": True, "data": news}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def get_news(self, session: AsyncSession, news_id: int) -> Dict[str, Any]:
        """获取新闻详情"""
        try:
            news = await crud_news.get(session, id=news_id)
            if not news:
                return {"success": False, "message": "新闻不存在"}
            return {"success": True, "data": news}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def get_news_list(
        self, 
        session: AsyncSession, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        author_id: Optional[UUID] = None,
        is_published: Optional[bool] = None
    ) -> Dict[str, Any]:
        """获取新闻列表"""
        try:
            news_list = await crud_news.get_multi(
                session, 
                skip=skip, 
                limit=limit,
                author_id=author_id,
                is_published=is_published
            )
            return {"success": True, "data": news_list}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def update_news(
        self, 
        session: AsyncSession, 
        *, 
        news_id: int, 
        obj_in: NewsUpdate
    ) -> Dict[str, Any]:
        """更新新闻"""
        try:
            news = await crud_news.get(session, id=news_id)
            if not news:
                return {"success": False, "message": "新闻不存在"}
            
            updated_news = await crud_news.update(session, db_obj=news, obj_in=obj_in)
            return {"success": True, "data": updated_news}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def delete_news(self, session: AsyncSession, news_id: int) -> Dict[str, Any]:
        """删除新闻"""
        try:
            news = await crud_news.delete(session, id=news_id)
            if not news:
                return {"success": False, "message": "新闻不存在"}
            return {"success": True, "data": news}
        except Exception as e:
            return {"success": False, "message": str(e)}


class OrderService:
    """订单服务类"""
    
    async def create_order(
        self, 
        session: AsyncSession, 
        *, 
        obj_in: OrderCreate, 
        customer_id: UUID
    ) -> Dict[str, Any]:
        """创建订单"""
        try:
            # 检查订单号是否已存在
            existing_order = await crud_order.get_by_order_no(session, order_no=obj_in.order_no)
            if existing_order:
                return {"success": False, "message": "订单号已存在"}
            
            order = await crud_order.create(session, obj_in=obj_in, customer_id=customer_id)
            return {"success": True, "data": order}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def get_order(self, session: AsyncSession, order_id: int) -> Dict[str, Any]:
        """获取订单详情"""
        try:
            order = await crud_order.get(session, id=order_id)
            if not order:
                return {"success": False, "message": "订单不存在"}
            return {"success": True, "data": order}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def get_order_list(
        self, 
        session: AsyncSession, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        customer_id: Optional[UUID] = None,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """获取订单列表"""
        try:
            order_list = await crud_order.get_multi(
                session, 
                skip=skip, 
                limit=limit,
                customer_id=customer_id,
                status=status
            )
            return {"success": True, "data": order_list}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def update_order(
        self, 
        session: AsyncSession, 
        *, 
        order_id: int, 
        obj_in: OrderUpdate
    ) -> Dict[str, Any]:
        """更新订单"""
        try:
            order = await crud_order.get(session, id=order_id)
            if not order:
                return {"success": False, "message": "订单不存在"}
            
            updated_order = await crud_order.update(session, db_obj=order, obj_in=obj_in)
            return {"success": True, "data": updated_order}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def delete_order(self, session: AsyncSession, order_id: int) -> Dict[str, Any]:
        """删除订单"""
        try:
            order = await crud_order.delete(session, id=order_id)
            if not order:
                return {"success": False, "message": "订单不存在"}
            return {"success": True, "data": order}
        except Exception as e:
            return {"success": False, "message": str(e)}


class ProductService:
    """产品服务类"""
    
    async def create_product(
        self, 
        session: AsyncSession, 
        *, 
        obj_in: ProductCreate
    ) -> Dict[str, Any]:
        """创建产品"""
        try:
            product = await crud_product.create(session, obj_in=obj_in)
            return {"success": True, "data": product}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def get_product(self, session: AsyncSession, product_id: int) -> Dict[str, Any]:
        """获取产品详情"""
        try:
            product = await crud_product.get(session, id=product_id)
            if not product:
                return {"success": False, "message": "产品不存在"}
            return {"success": True, "data": product}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def get_product_list(
        self, 
        session: AsyncSession, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        category_id: Optional[int] = None,
        is_active: Optional[bool] = None
    ) -> Dict[str, Any]:
        """获取产品列表"""
        try:
            product_list = await crud_product.get_multi(
                session, 
                skip=skip, 
                limit=limit,
                category_id=category_id,
                is_active=is_active
            )
            return {"success": True, "data": product_list}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def update_product(
        self, 
        session: AsyncSession, 
        *, 
        product_id: int, 
        obj_in: ProductUpdate
    ) -> Dict[str, Any]:
        """更新产品"""
        try:
            product = await crud_product.get(session, id=product_id)
            if not product:
                return {"success": False, "message": "产品不存在"}
            
            updated_product = await crud_product.update(session, db_obj=product, obj_in=obj_in)
            return {"success": True, "data": updated_product}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def delete_product(self, session: AsyncSession, product_id: int) -> Dict[str, Any]:
        """删除产品"""
        try:
            product = await crud_product.delete(session, id=product_id)
            if not product:
                return {"success": False, "message": "产品不存在"}
            return {"success": True, "data": product}
        except Exception as e:
            return {"success": False, "message": str(e)}


class ProductCategoryService:
    """产品分类服务类"""
    
    async def create_category(
        self, 
        session: AsyncSession, 
        *, 
        obj_in: ProductCategoryCreate
    ) -> Dict[str, Any]:
        """创建产品分类"""
        try:
            category = await crud_product_category.create(session, obj_in=obj_in)
            return {"success": True, "data": category}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def get_category(self, session: AsyncSession, category_id: int) -> Dict[str, Any]:
        """获取产品分类详情"""
        try:
            category = await crud_product_category.get(session, id=category_id)
            if not category:
                return {"success": False, "message": "产品分类不存在"}
            return {"success": True, "data": category}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def get_category_list(
        self, 
        session: AsyncSession, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        parent_id: Optional[int] = None,
        is_active: Optional[bool] = None
    ) -> Dict[str, Any]:
        """获取产品分类列表"""
        try:
            category_list = await crud_product_category.get_multi(
                session, 
                skip=skip, 
                limit=limit,
                parent_id=parent_id,
                is_active=is_active
            )
            return {"success": True, "data": category_list}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def get_category_tree(self, session: AsyncSession) -> Dict[str, Any]:
        """获取产品分类树"""
        try:
            category_tree = await crud_product_category.get_tree(session)
            return {"success": True, "data": category_tree}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def update_category(
        self, 
        session: AsyncSession, 
        *, 
        category_id: int, 
        obj_in: ProductCategoryUpdate
    ) -> Dict[str, Any]:
        """更新产品分类"""
        try:
            category = await crud_product_category.get(session, id=category_id)
            if not category:
                return {"success": False, "message": "产品分类不存在"}
            
            updated_category = await crud_product_category.update(session, db_obj=category, obj_in=obj_in)
            return {"success": True, "data": updated_category}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def delete_category(self, session: AsyncSession, category_id: int) -> Dict[str, Any]:
        """删除产品分类"""
        try:
            # 检查是否有子分类
            children = await crud_product_category.get_multi(session, parent_id=category_id)
            if children:
                return {"success": False, "message": "存在子分类，无法删除"}
            
            category = await crud_product_category.delete(session, id=category_id)
            if not category:
                return {"success": False, "message": "产品分类不存在"}
            return {"success": True, "data": category}
        except Exception as e:
            return {"success": False, "message": str(e)}


# 创建服务实例
news_service = NewsService()
order_service = OrderService()
product_service = ProductService()
product_category_service = ProductCategoryService()
