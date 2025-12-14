from sqlmodel import SQLModel

# Import all SQLModel models here to ensure Alembic can discover them
# 只要导入了，它们就会自动注册到 SQLModel.metadata 中。
# --- System 模块 ---
from app.system.models import (
    SysUser,
    SysRole,
    SysMenu,
    SysDict,
    SysDictData,
    SysUserRole,
    SysRoleMenu
)


# You might not need to do anything else here.
# Alembic will typically look at SQLModel.metadata for all registered models.
# The act of importing them makes them registered.
