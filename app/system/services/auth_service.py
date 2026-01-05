from datetime import datetime, timezone, timedelta
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.security import create_access_token, create_refresh_token, decode_token
from app.core.resp import Result
from app.core.config import settings  # 假设你有 settings 配置
from app.system.models import SysUser, SysUserToken
from app.system.schemas.auth import TokenSchema

class AuthService:

    async def login(self, session: AsyncSession, user: SysUser) -> Result[TokenSchema]:
        """
        登录成功后，生成双 Token 并持久化 Refresh Token
        """
        # 1. 生成 Access Token (无状态，不存库)
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id), "type": "access"},
            expires_delta=access_token_expires
        )

        # 2. 生成 Refresh Token (有状态，存库)
        refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        refresh_token = create_refresh_token(
            data={"sub": str(user.id), "type": "refresh"},
            expires_delta=refresh_token_expires
        )

        # 3. 持久化 Refresh Token 到数据库
        db_token = SysUserToken(
            user_id=user.id,
            token=refresh_token,
            expires_at=datetime.now(timezone.utc) + refresh_token_expires,
            is_used=False
        )
        session.add(db_token)
        await session.commit()

        # 4. 返回结果
        return Result.success(TokenSchema(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=access_token_expires.total_seconds()
        ))

    async def refresh_token(self, session: AsyncSession, token_in: str) -> Result[TokenSchema]:
        """
        令牌轮换逻辑：旧换新，检测重用
        """
        # 1. 基础校验
        payload = decode_token(token_in)
        if not payload or payload.get("type") != "refresh":
            return Result.error(401, "无效的刷新令牌")

        # 2. 查库
        stmt = select(SysUserToken).where(SysUserToken.token == token_in)
        result = await session.exec(stmt)
        db_token = result.first()

        if not db_token:
            # Token 虽然签名对，但在库里找不到 -> 可能是被恶意伪造或已被清理
            return Result.error(401, "令牌无效或已失效")

        # 3. 【核心安全检查】检测令牌重用 (Token Reuse Detection)
        if db_token.is_used:
            # === 安全警报 ===
            # 该令牌已被使用过，现在又被拿来刷新 -> 说明令牌泄露，有黑客在尝试重放
            # 策略：立即作废该用户所有的 Refresh Token，强制重新登录
            # await self.revoke_all_user_tokens(session, db_token.user_id)
            return Result.error(401, "安全警告：检测到异常令牌使用，请重新登录")

        # 4. 检查过期
        if db_token.expires_at < datetime.now(timezone.utc):
            return Result.error(401, "令牌已过期")

        # 5. 【轮换】标记当前 Token 为已使用
        db_token.is_used = True
        session.add(db_token)

        # 6. 签发全新的一对 Token
        # 这里需要查询用户对象来确保用户没被禁用 (可选)
        user = await session.get(SysUser, db_token.user_id)
        if not user or not user.is_active:
             return Result.error(401, "用户不存在或已被禁用")

        return await self.login(session, user)

    async def logout(self, session: AsyncSession, token_in: str) -> Result:
        """
        退出登录：将 Refresh Token 标记为已使用或删除
        """
        stmt = select(SysUserToken).where(SysUserToken.token == token_in)
        result = await session.exec(stmt)
        db_token = result.first()

        if db_token:
            # 标记为已使用，或者直接物理删除
            db_token.is_used = True
            session.add(db_token)
            await session.commit()

        return Result.success(msg="退出成功")

auth_service = AuthService()
