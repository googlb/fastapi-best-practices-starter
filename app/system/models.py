from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship
from app.db.mixins import BaseModel, SystemModel, FullAuditModel


class SysUser(FullAuditModel, table=True):
    """系统用户表 - 后台系统用户管理"""
    __tablename__ = "sys_users"
    __table_args__ = {"comment": "后台系统用户管理"}
    
    username: str = Field(unique=True, index=True, max_length=50, description="用户名")
    email: str = Field(unique=True, index=True, max_length=100, description="邮箱")
    hashed_password: str = Field(description="密码哈希值")
    is_active: bool = Field(default=True, description="是否激活")
    is_superuser: bool = Field(default=False, description="是否超级管理员")
    last_login_at: Optional[datetime] = Field(default=None, description="最后登录时间")
    remark: Optional[str] = Field(default=None, max_length=500, description="备注")


class SysRole(SystemModel, table=True):
    """角色表 - 系统角色管理"""
    __tablename__ = "sys_roles"
    __table_args__ = {"comment": "系统角色管理"}
    
    name: str = Field(unique=True, max_length=50, description="角色名称")
    code: str = Field(unique=True, max_length=50, description="角色编码")
    description: Optional[str] = Field(default=None, max_length=200, description="角色描述")
    
    # 关联关系
    users: list[SysUser] = Relationship(back_populates="role")
    menus: list["SysMenu"] = Relationship(back_populates="roles", link_model="SysRoleMenu")


class SysMenu(SystemModel, table=True):
    """菜单表 - 系统菜单管理"""
    __tablename__ = "sys_menus"
    __table_args__ = {"comment": "系统菜单管理"}
    
    title: str = Field(max_length=50, description="菜单标题")
    name: str = Field(max_length=50, description="菜单名称")
    path: Optional[str] = Field(default=None, max_length=200, description="路由路径")
    component: Optional[str] = Field(default=None, max_length=200, description="组件路径")
    icon: Optional[str] = Field(default=None, max_length=50, description="菜单图标")
    sort: int = Field(default=0, description="排序")
    parent_id: Optional[UUID] = Field(default=None, foreign_key="sys_menus.id", description="父菜单ID")
    menu_type: int = Field(default=1, description="菜单类型 1:目录 2:菜单 3:按钮")
    is_visible: bool = Field(default=True, description="是否显示")
    is_keep_alive: bool = Field(default=True, description="是否缓存")
    is_affix: bool = Field(default=False, description="是否固定")
    
    # 关联关系
    parent: Optional["SysMenu"] = Relationship(back_populates="children", sa_relationship_kwargs={"remote_side": "SysMenu.id"})
    children: list["SysMenu"] = Relationship(back_populates="parent")
    roles: list["SysRole"] = Relationship(back_populates="menus", link_model="SysRoleMenu")


class SysDict(SystemModel, table=True):
    """字典表 - 系统字典管理"""
    __tablename__ = "sys_dicts"
    __table_args__ = {"comment": "系统字典管理"}
    
    name: str = Field(max_length=50, description="字典名称")
    code: str = Field(unique=True, max_length=50, description="字典编码")
    description: Optional[str] = Field(default=None, max_length=200, description="字典描述")


class SysDictData(SystemModel, table=True):
    """字典数据表 - 系统字典数据管理"""
    __tablename__ = "sys_dict_data"
    __table_args__ = {"comment": "系统字典数据管理"}
    
    dict_id: UUID = Field(foreign_key="sys_dicts.id", description="字典ID")
    label: str = Field(max_length=100, description="字典标签")
    value: str = Field(max_length=100, description="字典值")
    sort: int = Field(default=0, description="排序")
    is_default: bool = Field(default=False, description="是否默认值")
    
    # 关联关系
    dict: SysDict = Relationship(back_populates="data")


class SysRoleMenu(BaseModel, table=True):
    """角色菜单关联表 - 角色与菜单的多对多关系"""
    __tablename__ = "sys_role_menus"
    __table_args__ = {"comment": "角色与菜单的多对多关系"}
    
    role_id: UUID = Field(foreign_key="sys_roles.id", primary_key=True, description="角色ID")
    menu_id: UUID = Field(foreign_key="sys_menus.id", primary_key=True, description="菜单ID")


# 添加反向关系
SysUser.role_id: Optional[UUID] = Field(default=None, foreign_key="sys_roles.id", description="角色ID")
SysUser.role: Optional[SysRole] = Relationship(back_populates="users")
SysDict.data: list[SysDictData] = Relationship(back_populates="dict")
