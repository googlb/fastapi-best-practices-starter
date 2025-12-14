from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import timedelta

from app.dependencies.database import get_async_session
from app.dependencies.auth import get_current_user
from app.domains.user.schemas import UserLogin, TokenResponse, UserResponse
from app.domains.user.crud import get_user_by_username
from app.core.security import verify_password, create_access_token, create_refresh_token
from app.domains.user.models import User

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: UserLogin,
    session: AsyncSession = Depends(get_async_session),
):
    """用户登录端点"""
    user = await get_user_by_username(session, credentials.username)
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive",
        )
    
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
):
    """获取当前用户信息"""
    return current_user
