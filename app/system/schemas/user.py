from pydantic import BaseModel, EmailStr, UUID4
from datetime import datetime
from typing import Optional


class SysUserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    remark: Optional[str] = None


class SysUserCreate(SysUserBase):
    password: str
    role_id: Optional[UUID4] = None


class SysUserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    remark: Optional[str] = None
    role_id: Optional[UUID4] = None
    password: Optional[str] = None


class SysUserResponse(SysUserBase):
    id: UUID4
    last_login_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    role_id: Optional[UUID4] = None
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
