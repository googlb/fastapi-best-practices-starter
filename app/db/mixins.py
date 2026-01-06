from datetime import datetime, timezone
from typing import Optional
from zoneinfo import ZoneInfo
from pydantic import ConfigDict
from sqlmodel import SQLModel, Field
import sqlalchemy as sa

# 定义北京时区
SHANGHAI_TZ = ZoneInfo("Asia/Shanghai")


# 2. 定义全局时间格式化函数
def datetime_formatter(dt: datetime) -> str:
    """
    将任何 datetime 对象转换为 'YYYY-MM-DD HH:MM:SS' 字符串
    """
    if dt is None:
        return None
    # 补全 UTC 时区 (防止 naive datetime 报错)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    # 转为北京时间并格式化
    return dt.astimezone(SHANGHAI_TZ).strftime("%Y-%m-%d %H:%M:%S")

# 3. 定义项目的核心基类 (替换原生的 SQLModel)
class BaseSQLModel(SQLModel):
    """
    项目所有 DB 模型的基类
    """
    model_config = ConfigDict(
        # 只要是 datetime 类型，无论是 created_at 还是 last_login_at，都会走这个逻辑
        json_encoders={
            datetime: datetime_formatter
        }
    )



# ==================== 基础功能 Mixin ====================

class TimestampMixin(SQLModel):
    created_at: datetime = Field(
        # 1. 【解决警告】使用 timezone-aware 的 UTC 时间
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=sa.DateTime(timezone=True),
        sa_column_kwargs={
            "server_default": sa.func.now(),
            "nullable": False,
            "comment": "创建时间"
        },
        description="创建时间"
    )

    updated_at: datetime = Field(
        # 1. 【解决警告】同上
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=sa.DateTime(timezone=True),
        sa_column_kwargs={
            "server_default": sa.func.now(),
            "onupdate": sa.func.now(),
            "nullable": False,
            "comment": "更新时间"
        },
        description="更新时间"
    )

# ==================== 核心基类 (Business Base Classes) ====================

class BaseModel(TimestampMixin, BaseSQLModel):
    """
    【基础模型】
    包含: ID(自增), 创建时间, 更新时间
    适用于: 大多数普通业务表
    """
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        index=True,
        description="ID"
    )


class SoftDeleteMixin(SQLModel):
    """
    软删除混入
    """
    is_deleted: bool = Field(
        default=False,
        sa_column_kwargs={"comment": "是否删除 0:否 1:是"},
        description="是否删除"
    )






class SystemModel(BaseModel):
    """
    【系统配置模型】
    包含: ID, 时间, 状态(status)
    适用于: 菜单, 字典, 角色, 部门
    """
    status: int = Field(
        default=1,
        sa_column_kwargs={"comment": "状态 1:启用 0:禁用"},
        description="状态"
    )


class FullAuditModel(BaseModel, SoftDeleteMixin):
    """
    【完整审计模型】
    包含: ID, 时间, 软删除, 创建人/更新人/删除人
    适用于: 用户表, 订单表, 支付记录
    """
    created_by: Optional[int] = Field(
        default=None,
        foreign_key="sys_users.id",
        sa_column_kwargs={"comment": "创建人ID"},
        description="创建人"
    )

    updated_by: Optional[int] = Field(
        default=None,
        foreign_key="sys_users.id",
        sa_column_kwargs={"comment": "更新人ID"},
        description="更新人"
    )

