import asyncio
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

# 1. 导入基础配置(仅需数据库连接)和日志
from app.core.config import settings
from loguru import logger

# 2. 导入业务模块
from app.system.crud.crud_user import crud_user
from app.system.schemas.user import SysUserCreate

# =======================================================
# 配置区域：默认超级管理员账号
# =======================================================
DEFAULT_ADMIN_USER = "admin"
DEFAULT_ADMIN_PWD = "password123"
DEFAULT_ADMIN_EMAIL = "admin@example.com"


# =======================================================
# 1. 初始化超级管理员逻辑
# =======================================================
async def init_superuser(session: AsyncSession) -> None:
    """
    初始化超级管理员
    """
    # 1. 检查是否存在
    user = await crud_user.get_by_username(session, username=DEFAULT_ADMIN_USER)

    if not user:
        logger.info(f"🚀 正在创建默认超级管理员账号: {DEFAULT_ADMIN_USER} ...")

        # 2. 组装数据
        user_in = SysUserCreate(
            username=DEFAULT_ADMIN_USER,
            password=DEFAULT_ADMIN_PWD,
            email=DEFAULT_ADMIN_EMAIL,
            nickname="超级管理员",
            is_active=True,
            is_superuser=True,
            role_ids=[]
        )

        # 3. 执行创建 (CRUD内部会自动处理密码Hash)
        user = await crud_user.create(session, obj_in=user_in)

        logger.success(f"✅ 超级管理员创建成功！")
        logger.info(f"   - 账号: {user.username}")
        logger.info(f"   - 密码: {DEFAULT_ADMIN_PWD}")
    else:
        logger.warning(f"⚠️ 超级管理员 {DEFAULT_ADMIN_USER} 已存在，跳过创建。")


# =======================================================
# 2. 脚本主入口
# =======================================================
async def main():
    logger.info("🔄 开始初始化数据库...")

    # 创建数据库引擎
    engine = create_async_engine(settings.DATABASE_URL, echo=False)

    # 创建 Session 工厂
    AsyncSessionLocal = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with AsyncSessionLocal() as session:
        await init_superuser(session)
        # 后续可在此处添加 await init_menus(session) 等

    await engine.dispose()
    logger.info("✨ 初始化完成！")


if __name__ == "__main__":
    asyncio.run(main())
