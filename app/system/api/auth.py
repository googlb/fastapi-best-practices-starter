from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from app.dependencies.database import get_session
from app.system.schemas.user import UserLogin
from app.system.services.user_service import sys_user_service
from app.core.security import create_access_token, create_refresh_token, decode_token
from app.core.resp import Result
from app.system.crud.crud_user import crud_user
from pydantic import BaseModel

router = APIRouter()

# 定义刷新 Token 的请求体
class RefreshTokenRequest(BaseModel):
    refreshToken: str

@router.post("/login", summary="用户登录")
async def login(
    credentials: UserLogin,
    session: AsyncSession = Depends(get_session),
):
    # 1. 验证用户名密码
    result = await sys_user_service.authenticate_user(
        session, credentials.username, credentials.password
    )
    if not result.is_success:
        return result

    user = result.data

    # 2. 签发 Token (注意：这里增加了 type 区分)
    access_token = create_access_token(data={"sub": str(user.id), "type": "access"})
    refresh_token = create_refresh_token(data={"sub": str(user.id), "type": "refresh"})

    # 3. 返回结果 (注意驼峰命名配合前端)
    return Result.success({
        "accessToken": access_token,
        "refreshToken": refresh_token,
    })

@router.post("/refresh", summary="刷新令牌")
async def refresh_token(
    request_data: RefreshTokenRequest,
    session: AsyncSession = Depends(get_session),
):
    # 1. 解码验证
    payload = decode_token(request_data.refreshToken)
    if not payload:
        return Result.error(401, "无效的刷新令牌")

    if payload.get("type") != "refresh":
        return Result.error(401, "令牌类型错误")

    user_id = payload.get("sub")

    # 2. 检查用户状态 (防止被封号的用户还能刷新)
    user = await crud_user.get(session, int(user_id))
    if not user:
        return Result.error(401, "用户不存在")
    if not user.is_active:
        return Result.error(401, "用户已被禁用")

    # 3. 签发新的 Access Token
    new_access_token = create_access_token(
        data={"sub": str(user.id), "type": "access"}
    )

    # 4. 可选：Token Rotation (同时也签发新的 refresh token)
    # new_refresh_token = create_refresh_token(data={"sub": str(user.id), "type": "refresh"})

    return Result.success({
        "accessToken": new_access_token,
        # "refreshToken": new_refresh_token # 如果开启 Token Rotation 则返回这个
    })

@router.post("/logout", summary="退出登录")
async def logout():
    # JWT 是无状态的，后端其实不需要做太多操作。
    # 但如果有 Redis 黑名单机制，可以在这里把 token 加入黑名单。
    return Result.success(msg="退出成功")
