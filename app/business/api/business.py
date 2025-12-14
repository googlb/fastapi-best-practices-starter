from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID

from app.dependencies.database import get_session
from app.dependencies.auth import get_current_user
from app.business.schemas.business import (
    NewsCreate, NewsUpdate, NewsResponse,
    OrderCreate, OrderUpdate, OrderResponse,
    ProductCreate, ProductUpdate, ProductResponse,
    ProductCategoryCreate, ProductCategoryUpdate, ProductCategoryResponse
)
from app.business.services.business_service import (
    news_service, order_service, product_service, product_category_service
)
from app.system.models import SysUser
from app.core.result import Result, PageResult

router = APIRouter(prefix="/business", tags=["业务"])


# 新闻相关路由
news_router = APIRouter(prefix="/news", tags=["业务-新闻"])

@news_router.post("/")
async def create_news(
    *,
    session: AsyncSession = Depends(get_session),
    news_in: NewsCreate,
    current_user: SysUser = Depends(get_current_user)
):
    """创建新闻"""
    result = await news_service.create_news(session, obj_in=news_in, author_id=current_user.id)
    
    if not result["success"]:
        return Result.error(400, result["message"])
    
    return Result.success(result["data"])


@news_router.get("/{news_id}")
async def get_news(
    news_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: SysUser = Depends(get_current_user)
):
    """获取新闻详情"""
    result = await news_service.get_news(session, news_id)
    
    if not result["success"]:
        return Result.error(404, result["message"])
    
    return Result.success(result["data"])


@news_router.get("/")
async def get_news_list(
    session: AsyncSession = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
    is_published: bool = True,
    current_user: SysUser = Depends(get_current_user)
):
    """获取新闻列表"""
    result = await news_service.get_news_list(
        session, 
        skip=skip, 
        limit=limit,
        is_published=is_published
    )
    
    if not result["success"]:
        return Result.error(400, result["message"])
    
    # 如果有总数信息，使用PageResult
    if "total" in result:
        return PageResult.success(result["data"], result["total"], skip//limit + 1, limit)
    return Result.success(result["data"])


@news_router.put("/{news_id}")
async def update_news(
    *,
    session: AsyncSession = Depends(get_session),
    news_id: int,
    news_in: NewsUpdate,
    current_user: SysUser = Depends(get_current_user)
):
    """更新新闻"""
    result = await news_service.update_news(session, news_id=news_id, obj_in=news_in)
    
    if not result["success"]:
        return Result.error(400, result["message"])
    
    return Result.success(result["data"])


@news_router.delete("/{news_id}")
async def delete_news(
    news_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: SysUser = Depends(get_current_user)
):
    """删除新闻"""
    result = await news_service.delete_news(session, news_id)
    
    if not result["success"]:
        return Result.error(404, result["message"])
    
    return Result.success({"message": "新闻删除成功"})


# 订单相关路由
order_router = APIRouter(prefix="/orders", tags=["业务-订单"])

@order_router.post("/")
async def create_order(
    *,
    session: AsyncSession = Depends(get_session),
    order_in: OrderCreate,
    current_user: SysUser = Depends(get_current_user)
):
    """创建订单"""
    result = await order_service.create_order(session, obj_in=order_in, customer_id=current_user.id)
    
    if not result["success"]:
        return Result.error(400, result["message"])
    
    return Result.success(result["data"])


@order_router.get("/{order_id}")
async def get_order(
    order_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: SysUser = Depends(get_current_user)
):
    """获取订单详情"""
    result = await order_service.get_order(session, order_id)
    
    if not result["success"]:
        return Result.error(404, result["message"])
    
    return Result.success(result["data"])


@order_router.get("/")
async def get_order_list(
    session: AsyncSession = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
    current_user: SysUser = Depends(get_current_user)
):
    """获取订单列表"""
    result = await order_service.get_order_list(
        session, 
        skip=skip, 
        limit=limit,
        customer_id=current_user.id
    )
    
    if not result["success"]:
        return Result.error(400, result["message"])
    
    # 如果有总数信息，使用PageResult
    if "total" in result:
        return PageResult.success(result["data"], result["total"], skip//limit + 1, limit)
    return Result.success(result["data"])


@order_router.put("/{order_id}")
async def update_order(
    *,
    session: AsyncSession = Depends(get_session),
    order_id: int,
    order_in: OrderUpdate,
    current_user: SysUser = Depends(get_current_user)
):
    """更新订单"""
    result = await order_service.update_order(session, order_id=order_id, obj_in=order_in)
    
    if not result["success"]:
        return Result.error(400, result["message"])
    
    return Result.success(result["data"])


@order_router.delete("/{order_id}")
async def delete_order(
    order_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: SysUser = Depends(get_current_user)
):
    """删除订单"""
    result = await order_service.delete_order(session, order_id)
    
    if not result["success"]:
        return Result.error(404, result["message"])
    
    return Result.success({"message": "订单删除成功"})


# 产品相关路由
product_router = APIRouter(prefix="/products", tags=["业务-产品"])

@product_router.post("/")
async def create_product(
    *,
    session: AsyncSession = Depends(get_session),
    product_in: ProductCreate,
    current_user: SysUser = Depends(get_current_user)
):
    """创建产品"""
    result = await product_service.create_product(session, obj_in=product_in)
    
    if not result["success"]:
        return Result.error(400, result["message"])
    
    return Result.success(result["data"])


@product_router.get("/{product_id}")
async def get_product(
    product_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: SysUser = Depends(get_current_user)
):
    """获取产品详情"""
    result = await product_service.get_product(session, product_id)
    
    if not result["success"]:
        return Result.error(404, result["message"])
    
    return Result.success(result["data"])


@product_router.get("/")
async def get_product_list(
    session: AsyncSession = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
    current_user: SysUser = Depends(get_current_user)
):
    """获取产品列表"""
    result = await product_service.get_product_list(
        session, 
        skip=skip, 
        limit=limit
    )
    
    if not result["success"]:
        return Result.error(400, result["message"])
    
    # 如果有总数信息，使用PageResult
    if "total" in result:
        return PageResult.success(result["data"], result["total"], skip//limit + 1, limit)
    return Result.success(result["data"])


@product_router.put("/{product_id}")
async def update_product(
    *,
    session: AsyncSession = Depends(get_session),
    product_id: int,
    product_in: ProductUpdate,
    current_user: SysUser = Depends(get_current_user)
):
    """更新产品"""
    result = await product_service.update_product(session, product_id=product_id, obj_in=product_in)
    
    if not result["success"]:
        return Result.error(400, result["message"])
    
    return Result.success(result["data"])


@product_router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: SysUser = Depends(get_current_user)
):
    """删除产品"""
    result = await product_service.delete_product(session, product_id)
    
    if not result["success"]:
        return Result.error(404, result["message"])
    
    return Result.success({"message": "产品删除成功"})


# 产品分类相关路由
product_category_router = APIRouter(prefix="/product-categories", tags=["业务-产品分类"])

@product_category_router.post("/")
async def create_product_category(
    *,
    session: AsyncSession = Depends(get_session),
    category_in: ProductCategoryCreate,
    current_user: SysUser = Depends(get_current_user)
):
    """创建产品分类"""
    result = await product_category_service.create_product_category(session, obj_in=category_in)
    
    if not result["success"]:
        return Result.error(400, result["message"])
    
    return Result.success(result["data"])


@product_category_router.get("/{category_id}")
async def get_product_category(
    category_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: SysUser = Depends(get_current_user)
):
    """获取产品分类详情"""
    result = await product_category_service.get_product_category(session, category_id)
    
    if not result["success"]:
        return Result.error(404, result["message"])
    
    return Result.success(result["data"])


@product_category_router.get("/")
async def get_product_category_list(
    session: AsyncSession = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
    current_user: SysUser = Depends(get_current_user)
):
    """获取产品分类列表"""
    result = await product_category_service.get_product_category_list(
        session, 
        skip=skip, 
        limit=limit
    )
    
    if not result["success"]:
        return Result.error(400, result["message"])
    
    # 如果有总数信息，使用PageResult
    if "total" in result:
        return PageResult.success(result["data"], result["total"], skip//limit + 1, limit)
    return Result.success(result["data"])


@product_category_router.put("/{category_id}")
async def update_product_category(
    *,
    session: AsyncSession = Depends(get_session),
    category_id: int,
    category_in: ProductCategoryUpdate,
    current_user: SysUser = Depends(get_current_user)
):
    """更新产品分类"""
    result = await product_category_service.update_product_category(session, category_id=category_id, obj_in=category_in)
    
    if not result["success"]:
        return Result.error(400, result["message"])
    
    return Result.success(result["data"])


@product_category_router.delete("/{category_id}")
async def delete_product_category(
    category_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: SysUser = Depends(get_current_user)
):
    """删除产品分类"""
    result = await product_category_service.delete_product_category(session, category_id)
    
    if not result["success"]:
        return Result.error(404, result["message"])
    
    return Result.success({"message": "产品分类删除成功"})


# 将所有子路由器添加到主路由器
router.include_router(news_router)
router.include_router(order_router)
router.include_router(product_router)
router.include_router(product_category_router)
