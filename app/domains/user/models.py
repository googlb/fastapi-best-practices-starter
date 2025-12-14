from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Optional


class User(SQLModel, table=True):
    """用户表 - 后台系统用户管理"""
    __tablename__ = "users"
    __table_args__ = {"comment": "后台系统用户管理"}
    
    id: Optional[int] = Field(default=None, primary_key=True, description="用户ID")
    username: str = Field(unique=True, index=True, description="用户名")
    email: str = Field(unique=True, index=True, description="邮箱")
    hashed_password: str = Field(description="密码哈希值")
    is_active: bool = Field(default=True, description="是否激活")
    is_superuser: bool = Field(default=False, description="是否超级管理员")
    last_login_at: Optional[datetime] = Field(default=None, description="最后登录时间")
    remark: Optional[str] = Field(default=None, max_length=500, description="备注")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="更新时间")
