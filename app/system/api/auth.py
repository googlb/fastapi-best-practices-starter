from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

# 依赖注入
from app.dependencies.database import get_session
from app.core.resp import Result

# 业务逻辑与 Schema
from app.system.services.user_service import sys_user_service
from app.system.services.auth_service import auth_service
from app.system.schemas.auth import UserLogin, TokenSchema, RefreshTokenRequest

router = APIRouter()

@router.post(
    "/login",
    summary="用户登录",
    description="使用用户名和密码登录，获取 Access Token 和 Refresh Token",
    response_model=Result[TokenSchema]
)
async def login(
    credentials: UserLogin,
    session: AsyncSession = Depends(get_session),
) -> Result[TokenSchema]:
    """
    用户登录
    """
    # 1. 校验账号密码 (使用 User Service)
    auth_result = await sys_user_service.authenticate_user(
        session, credentials.username, credentials.password
    )

    if not auth_result.is_success:
        return auth_result  # 返回 401 或 403 错误 Result

    user = auth_result.data

    # 2. 生成令牌并持久化 (使用 Auth Service)
    return await auth_service.login(session, user)


@router.post(
    "/refresh",
    summary="刷新令牌",
    description="使用 Refresh Token 获取新的 Access Token (支持自动轮换)",
    response_model=Result[TokenSchema]
)
async def refresh_token(
    request_data: RefreshTokenRequest,
    session: AsyncSession = Depends(get_session),
) -> Result[TokenSchema]:
    """
    刷新 Token (轮换模式)
    """
    return await auth_service.refresh_token(session, request_data.refresh_token)


@router.post(
    "/logout",
    summary="退出登录",
    description="作废当前的 Refresh Token",
    response_model=Result[str]
)
async def logout(
    request_data: RefreshTokenRequest,
    session: AsyncSession = Depends(get_session),
) -> Result[str]:
    """
    退出登录
    """
    return await auth_service.logout(session, request_data.refresh_token)
