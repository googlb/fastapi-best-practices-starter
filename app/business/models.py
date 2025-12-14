from typing import Optional, TYPE_CHECKING
from datetime import datetime
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship
from app.db.mixins import BaseModel, FullAuditModel

if TYPE_CHECKING:
    from app.system.models import SysUser


class News(BaseModel, table=True):
    """新闻表 - 新闻资讯管理"""
    __tablename__ = "biz_news"
    __table_args__ = {"comment": "新闻资讯管理"}
    
    title: str = Field(index=True, max_length=200, description="新闻标题")
    content: str = Field(description="新闻内容")
    author_id: Optional[UUID] = Field(default=None, foreign_key="sys_users.id", description="作者ID")
    is_published: bool = Field(default=False, description="是否发布")
    published_at: Optional[datetime] = Field(default=None, description="发布时间")
    view_count: int = Field(default=0, description="浏览次数")
    
    # 关联关系
    author: Optional["SysUser"] = Relationship(back_populates="news")


class Order(FullAuditModel, table=True):
    """订单表 - 业务订单管理"""
    __tablename__ = "biz_orders"
    __table_args__ = {"comment": "业务订单管理"}
    
    order_no: str = Field(unique=True, max_length=50, description="订单编号")
    total_amount: float = Field(description="订单总金额")
    status: int = Field(default=1, description="订单状态 1:待支付 2:已支付 3:已发货 4:已完成 5:已取消")
    payment_method: Optional[str] = Field(default=None, max_length=50, description="支付方式")
    payment_time: Optional[datetime] = Field(default=None, description="支付时间")
    delivery_time: Optional[datetime] = Field(default=None, description="发货时间")
    completion_time: Optional[datetime] = Field(default=None, description="完成时间")
    cancel_time: Optional[datetime] = Field(default=None, description="取消时间")
    cancel_reason: Optional[str] = Field(default=None, max_length=500, description="取消原因")
    
    # 关联关系
    user_id: Optional[UUID] = Field(default=None, foreign_key="sys_users.id", description="用户ID")
    user: Optional["SysUser"] = Relationship(back_populates="orders")


class Product(BaseModel, table=True):
    """产品表 - 产品信息管理"""
    __tablename__ = "biz_products"
    __table_args__ = {"comment": "产品信息管理"}
    
    name: str = Field(index=True, max_length=200, description="产品名称")
    description: Optional[str] = Field(default=None, max_length=1000, description="产品描述")
    price: float = Field(description="产品价格")
    stock: int = Field(default=0, description="库存数量")
    is_active: bool = Field(default=True, description="是否启用")
    category_id: Optional[UUID] = Field(default=None, foreign_key="biz_categories.id", description="分类ID")
    
    # 关联关系
    category: Optional["ProductCategory"] = Relationship(back_populates="products")


class ProductCategory(BaseModel, table=True):
    """产品分类表 - 产品分类管理"""
    __tablename__ = "biz_categories"
    __table_args__ = {"comment": "产品分类管理"}
    
    name: str = Field(unique=True, max_length=100, description="分类名称")
    description: Optional[str] = Field(default=None, max_length=500, description="分类描述")
    parent_id: Optional[UUID] = Field(default=None, foreign_key="biz_categories.id", description="父分类ID")
    sort: int = Field(default=0, description="排序")
    
    # 关联关系
    parent: Optional["ProductCategory"] = Relationship(back_populates="children", sa_relationship_kwargs={"remote_side": "ProductCategory.id"})
    children: list["ProductCategory"] = Relationship(back_populates="parent")


# 添加反向关系
SysUser.news: list[News] = Relationship(back_populates="author")
SysUser.orders: list[Order] = Relationship(back_populates="user")
