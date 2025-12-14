from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field
import sqlalchemy as sa


# ==================== 基础功能 Mixin ====================

class TimestampMixin(SQLModel):
    """
    通用时间戳混入
    """
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=sa.Column(
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
            comment="创建时间"
        ),
        description="创建时间"
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=sa.Column(
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
            comment="更新时间"
        ),
        description="更新时间"
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
    deleted_at: Optional[datetime] = Field(
        default=None,
        sa_column_kwargs={"comment": "删除时间"},
        description="删除时间"
    )


# ==================== 核心基类 (Business Base Classes) ====================

class BaseModel(TimestampMixin, SQLModel):
    """
    【基础模型】
    包含: ID(自增), 创建时间, 更新时间
    适用于: 大多数普通业务表
    """
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        index=True,
        description="主键ID"
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
    适用于: 用户表, 订单表, 支付记录 (核心业务数据)
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

    deleted_by: Optional[int] = Field(
        default=None,
        foreign_key="sys_users.id",
        sa_column_kwargs={"comment": "删除人ID"},
        description="删除人"
    )
