from datetime import datetime

from pydantic import BaseModel

from app.core.base_schema import BaseSchema


class MenuBase(BaseSchema):
    title: str
    name: str
    path: str | None = None
    component: str | None = None
    icon: str | None = None
    sort: int = 0
    parent_id: int | None = None
    menu_type: int = 1
    is_visible: bool = True
    is_keep_alive: bool = True
    status: int = 1


class MenuCreate(MenuBase):
    pass


class MenuUpdate(BaseModel):
    title: str | None = None
    name: str | None = None
    path: str | None = None
    component: str | None = None
    icon: str | None = None
    sort: int | None = None
    parent_id: int | None = None
    menu_type: int | None = None
    is_visible: bool | None = None
    is_keep_alive: bool | None = None
    status: int | None = None


class MenuResponse(MenuBase):
    id: int
    created_at: datetime
    updated_at: datetime
    children: list["MenuResponse"] | None = None

    class Config:
        from_attributes = True


# 解决前向引用
MenuResponse.model_rebuild()
