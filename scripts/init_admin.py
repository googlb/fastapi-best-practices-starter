import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.domains.user.crud import create_user, get_user_by_username


async def init_admin():
    """初始化 admin 用户"""
    engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)
    
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        # 检查 admin 用户是否已存在
        existing_admin = await get_user_by_username(session, "admin")
        if existing_admin:
            print("✓ Admin user already exists")
            return
        
        # 创建 admin 用户
        admin = await create_user(
            session=session,
            username="admin",
            email="admin@example.com",
            password="admin123",
            is_superuser=True,
        )
        print(f"✓ Admin user created successfully")
        print(f"  Username: {admin.username}")
        print(f"  Email: {admin.email}")
        print(f"  ID: {admin.id}")
    
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(init_admin())
