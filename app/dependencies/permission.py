from fastapi import Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List

from app.dependencies.database import get_session
from app.dependencies.auth import get_current_user
from app.system.models import SysUser
from app.system.services.permission_service import permission_service
# 假设你有一个 Redis 客户端封装
# from app.core.cache import redis_client

class Perms:
    """
    权限依赖注入类
    用法: dependencies=[Depends(Perms("system:user:add"))]
    """
    def __init__(self, permission: str):
        self.permission = permission

    async def __call__(
        self,
        user: SysUser = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
    ):
        """
        FastAPI 会自动调用这个方法进行验证
        """
        # 1. 超级管理员直接放行
        if user.is_superuser:
            return True

        # 2. 【最佳实践】优先从 Redis 获取权限列表 (伪代码)
        # cache_key = f"user_perms:{user.id}"
        # cached_perms = await redis_client.get(cache_key)
        # if cached_perms:
        #     user_perms = json.loads(cached_perms)
        # else:
        #     # 缓存未命中，查库并写入缓存
        #     user_perms = await permission_service.get_user_permissions(session, user.id)
        #     await redis_client.set(cache_key, json.dumps(user_perms), ex=3600)

        # --- 暂时使用直接查库演示 (生产环境建议加上面的 Redis) ---
        user_perms = await permission_service.get_user_permissions(session, user.id)

        # 3. 校验权限
        # 兼容性处理：有些前端框架可能用 *:*:* 代表所有权限，这里只做精确匹配
        if self.permission not in user_perms:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"权限不足，需要权限: {self.permission}"
            )

        return True
