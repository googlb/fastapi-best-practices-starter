from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from app.db.mixins import BaseModel, SystemModel, FullAuditModel

# ===========================================================================
# 关联表 (Link Tables) - 外键全部改为 int
# ===========================================================================

class SysUserRole(BaseModel, table=True):
    """用户角色关联表"""
    __tablename__ = "sys_user_roles"
    __table_args__ = {"comment": "用户与角色的多对多关系"}

    user_id: int = Field(foreign_key="sys_users.id", primary_key=True, description="用户ID")
    role_id: int = Field(foreign_key="sys_roles.id", primary_key=True, description="角色ID")


class SysRoleMenu(BaseModel, table=True):
    """角色菜单关联表"""
    __tablename__ = "sys_role_menus"
    __table_args__ = {"comment": "角色与菜单的多对多关系"}

    role_id: int = Field(foreign_key="sys_roles.id", primary_key=True, description="角色ID")
    menu_id: int = Field(foreign_key="sys_menus.id", primary_key=True, description="菜单ID")


# ===========================================================================
# 实体表 (Entities)
# ===========================================================================

class SysUser(BaseModel, table=True):
    """系统用户表"""
    __tablename__ = "sys_users"
    __table_args__ = {"comment": "后台系统用户管理"}

    username: str = Field(unique=True, index=True, max_length=50, description="用户名")
    email: Optional[str] = Field(default=None, unique=True, index=True, max_length=100, description="邮箱")
    hashed_password: str = Field(description="密码哈希值")
    is_active: bool = Field(default=True, description="是否激活")
    is_superuser: bool = Field(default=False, description="是否超级管理员")
    last_login_at: Optional[datetime] = Field(default=None, description="最后登录时间")
    remark: Optional[str] = Field(default=None, max_length=500, description="备注")

    # 关系 (M:N)
    roles: List["SysRole"] = Relationship(back_populates="users", link_model=SysUserRole)


class SysRole(SystemModel, table=True):
    """角色表"""
    __tablename__ = "sys_roles"
    __table_args__ = {"comment": "系统角色管理"}

    name: str = Field(max_length=50, description="角色名称")
    code: str = Field(unique=True, max_length=50, description="角色编码")
    description: Optional[str] = Field(default=None, max_length=200, description="角色描述")

    # 关系
    users: List[SysUser] = Relationship(back_populates="roles", link_model=SysUserRole)
    menus: List["SysMenu"] = Relationship(back_populates="roles", link_model=SysRoleMenu)


class SysMenu(SystemModel, table=True):
    """菜单表"""
    __tablename__ = "sys_menus"
    __table_args__ = {"comment": "系统菜单管理"}

    parent_id: Optional[int] = Field(default=None, foreign_key="sys_menus.id", description="父菜单ID")
    title: str = Field(max_length=50, description="菜单标题")
    name: Optional[str] = Field(default=None, max_length=50, description="路由名称")
    path: Optional[str] = Field(default=None, max_length=200, description="路由路径")
    component: Optional[str] = Field(default=None, max_length=200, description="组件路径")
    icon: Optional[str] = Field(default=None, max_length=50, description="图标")
    sort: int = Field(default=0, description="排序")
    permission: Optional[str] = Field(default=None, max_length=100, index=True, description="权限标识")
    menu_type: int = Field(default=1, description="类型 1:目录 2:菜单 3:按钮")
    is_visible: bool = Field(default=True, description="是否显示")
    is_keep_alive: bool = Field(default=True, description="是否缓存")
    status: int = Field(default=1, description="状态 1:正常 0:禁用")

    # 关系
    parent: Optional["SysMenu"] = Relationship(
        back_populates="children",
        sa_relationship_kwargs={"remote_side": "SysMenu.id"}
    )
    children: List["SysMenu"] = Relationship(back_populates="parent")
    roles: List[SysRole] = Relationship(back_populates="menus", link_model=SysRoleMenu)


class SysDict(SystemModel, table=True):
    """字典类型表"""
    __tablename__ = "sys_dicts"
    __table_args__ = {"comment": "系统字典管理"}

    name: str = Field(max_length=50, description="字典名称")
    code: str = Field(unique=True, max_length=50, description="字典编码")
    description: Optional[str] = Field(default=None, max_length=200, description="描述")

    # 关系
    data: List["SysDictData"] = Relationship(
        back_populates="dict",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class SysDictData(SystemModel, table=True):
    """字典数据表"""
    __tablename__ = "sys_dict_data"
    __table_args__ = {"comment": "系统字典数据管理"}

    dict_id: int = Field(foreign_key="sys_dicts.id", ondelete="CASCADE", description="字典ID")
    label: str = Field(max_length=100, description="展示标签")
    value: str = Field(max_length=100, description="字典值")
    sort: int = Field(default=0, description="排序")
    is_default: bool = Field(default=False, description="是否默认值")
    class_name: Optional[str] = Field(default=None, max_length=50, description="样式属性")

    # 关系
    dict: SysDict = Relationship(back_populates="data")
