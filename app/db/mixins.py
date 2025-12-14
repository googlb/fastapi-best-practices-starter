# app/db/mixins.py
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
import sqlalchemy as sa


class TimestampMixin(SQLModel):
    """时间戳混入（你已经写好的）"""
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=sa.Column(
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
            comment="创建时间"
        )
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=sa.Column(
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
            comment="更新时间"
        )
    )


class SoftDeleteMixin(SQLModel):
    """软删除混入（扩展版）"""
    is_deleted: bool = Field(
        default=False,
        sa_column_kwargs={"comment": "是否删除 0:否 1:是"}
    )
    deleted_at: Optional[datetime] = Field(
        default=None,
        sa_column_kwargs={"comment": "删除时间"}
    )


# ==================== 组合 Mixin ====================

class BaseModel(SQLModel):
    """基础模型 - 大部分表使用这个"""
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=sa.Column(
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
            comment="创建时间"
        )
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=sa.Column(
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
            comment="更新时间"
        )
    )


class SystemModel(BaseModel):
    """系统配置模型 - 菜单/字典/角色使用"""
    status: int = Field(
        default=1,
        sa_column_kwargs={"comment": "状态 1:启用 0:禁用"}
    )


class FullAuditModel(BaseModel, SoftDeleteMixin):
    """完整审计模型 - 用户/订单/支付使用"""
    created_by: Optional[UUID] = Field(
        default=None,
        foreign_key="sys_users.id",
        sa_column_kwargs={"comment": "创建人"}
    )
    updated_by: Optional[UUID] = Field(
        default=None,
        foreign_key="sys_users.id",
        sa_column_kwargs={"comment": "更新人"}
    )
    deleted_by: Optional[UUID] = Field(
        default=None,
        foreign_key="sys_users.id",
        sa_column_kwargs={"comment": "删除人"}
    )
