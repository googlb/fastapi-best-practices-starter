from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from app.core.base_schema import BaseSchema


class MenuBase(BaseSchema):
    title: str
    name: str
    path: Optional[str] = None
    component: Optional[str] = None
    icon: Optional[str] = None
    sort: int = 0
    parent_id: Optional[int] = None
    menu_type: int = 1
    is_visible: bool = True
    is_keep_alive: bool = True
    status: int = 1


class MenuCreate(MenuBase):
    pass


class MenuUpdate(BaseModel):
    title: Optional[str] = None
    name: Optional[str] = None
    path: Optional[str] = None
    component: Optional[str] = None
    icon: Optional[str] = None
    sort: Optional[int] = None
    parent_id: Optional[int] = None
    menu_type: Optional[int] = None
    is_visible: Optional[bool] = None
    is_keep_alive: Optional[bool] = None
    status: Optional[int] = None


class MenuResponse(MenuBase):
    id: int
    created_at: datetime
    updated_at: datetime
    children: Optional[List["MenuResponse"]] = None

    class Config:
        from_attributes = True


# 解决前向引用
MenuResponse.model_rebuild()
