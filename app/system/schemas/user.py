from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.core.base_schema import BaseSchema


class SysUserBase(BaseSchema):
    username: str
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    remark: str | None = None


class SysUserCreate(SysUserBase):
    password: str
    role_ids: list[int] | None = None


class SysUserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None
    remark: str | None = None
    role_ids: list[int] | None = None
    password: str | None = None


class SysUserResponse(SysUserBase):
    id: int
    last_login_at: datetime | None = None
    created_at: datetime
    updated_at: datetime
    role_ids: list[int] | None = None

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str
