from datetime import datetime

from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str
    code: str
    description: str | None = None
    status: int = 1


class RoleCreate(RoleBase):
    pass


class RoleUpdate(BaseModel):
    name: str | None = None
    code: str | None = None
    description: str | None = None
    status: int | None = None


class RoleResponse(RoleBase):
    id: int
    created_at: datetime
    updated_at: datetime
    menu_ids: list[int] | None = None

    class Config:
        from_attributes = True
