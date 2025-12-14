from sqlmodel import SQLModel

# Import all SQLModel models here to ensure Alembic can discover them
# 按依赖顺序导入: Level 0 (无外键依赖) -> Level 1 (依赖 Level 0) -> Level 2 (依赖 Level 1)

# Level 0 (无外键依赖)
from app.system.models import Role, Menu, Dict, DictData

# Level 1 (依赖 Level 0)
from app.system.models import SysUser

# Level 2 (依赖 Level 1)
from app.business.models import News, Order, Product, ProductCategory

# You might not need to do anything else here.
# Alembic will typically look at SQLModel.metadata for all registered models.
# The act of importing them makes them registered.
