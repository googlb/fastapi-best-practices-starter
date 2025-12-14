from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.domains.user.models import User
from app.core.security import hash_password


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    statement = select(User).where(User.username == username)
    result = await session.exec(statement)
    return result.scalar_one_or_none()


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    statement = select(User).where(User.id == user_id)
    result = await session.exec(statement)
    return result.scalar_one_or_none()


async def create_user(
    session: AsyncSession,
    username: str,
    email: str,
    password: str,
    is_superuser: bool = False,
) -> User:
    user = User(
        username=username,
        email=email,
        hashed_password=hash_password(password),
        is_superuser=is_superuser,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
