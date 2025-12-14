from typing import Optional, List
from sqlmodel import SQLModel
from datetime import datetime
from uuid import UUID


class NewsBase(SQLModel):
    title: str
    content: str
    summary: Optional[str] = None
    is_published: bool = False


class NewsCreate(NewsBase):
    pass


class NewsUpdate(SQLModel):
    title: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    is_published: Optional[bool] = None


class NewsResponse(NewsBase):
    id: int
    author_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class OrderBase(SQLModel):
    order_no: str
    total_amount: float
    status: str = "pending"
    notes: Optional[str] = None


class OrderCreate(OrderBase):
    pass


class OrderUpdate(SQLModel):
    total_amount: Optional[float] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class OrderResponse(OrderBase):
    id: int
    customer_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ProductBase(SQLModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int = 0
    is_active: bool = True
    category_id: Optional[int] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    is_active: Optional[bool] = None
    category_id: Optional[int] = None


class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ProductCategoryBase(SQLModel):
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None
    sort_order: int = 0
    is_active: bool = True


class ProductCategoryCreate(ProductCategoryBase):
    pass


class ProductCategoryUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[int] = None
    sort_order: Optional[int] = None
    is_active: Optional[bool] = None


class ProductCategoryResponse(ProductCategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime
    children: List["ProductCategoryResponse"] = []
    
    class Config:
        from_attributes = True

# 解决前向引用
ProductCategoryResponse.model_rebuild()
