import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
from alembic.operations import ops  # 【关键】需要导入 ops 用于识别操作类型

# 导入我们的配置和模型注册表
from app.core.config import settings
from app.db.base import SQLModel  # 【关键】加载所有模型的 metadata

config = context.config

# 【推荐】注释掉 fileConfig（我们用 loguru 统一日志）
# if config.config_file_name is not None:
#     fileConfig(config.config_file_name)

# 直接使用异步 URL (转为字符串以确保兼容性)
config.set_main_option("sqlalchemy.url", str(settings.DATABASE_URL))

target_metadata = SQLModel.metadata


# =======================================================
# 1. 定义字段排序逻辑 (Hook 函数)
# =======================================================
def reorder_columns(context, revision, directives):
    """
    拦截迁移指令，自动调整字段顺序：
    1. id 排在第一位
    2. 审计字段 (时间、软删除等) 排在最后一位
    """
    # 定义想要排在最后的字段名
    audit_cols = {
        'remark',
        'is_deleted',
        'created_at', 'updated_at',
        'created_by', 'updated_by',
    }

    # 定义想要排在最前的字段名
    start_cols = {'id'}

    # 遍历所有的迁移指令
    for directive in directives:
        if isinstance(directive, ops.MigrationScript):
            for upgrade_op in directive.upgrade_ops.ops:
                # 只处理 "创建表" (CreateTableOp) 的操作
                if isinstance(upgrade_op, ops.CreateTableOp):
                    cols = upgrade_op.columns

                    first_cols = []
                    middle_cols = []
                    last_cols = []

                    for col in cols:
                        name = col.name
                        if name in start_cols:
                            first_cols.append(col)
                        elif name in audit_cols:
                            last_cols.append(col)
                        else:
                            middle_cols.append(col)

                    # 重新组合顺序: ID -> 业务字段 -> 审计字段
                    # 修改原指令中的 columns 列表
                    upgrade_op.columns = first_cols + middle_cols + last_cols


# =======================================================
# 2. 迁移逻辑
# =======================================================

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # 即使是离线模式，建议也可以加上排序钩子（可选）
        process_revision_directives=reorder_columns,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        # 【关键】注册排序钩子
        process_revision_directives=reorder_columns,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations():
    """在线模式下使用异步引擎运行迁移"""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online():
    """在线模式入口"""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
