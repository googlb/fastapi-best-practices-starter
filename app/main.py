# app/main.py
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.v1.router import api_v1_router
from app.core.config import settings
from app.core.docs import register_docs
from app.core.exceptions import (
    BusinessException,
    business_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from app.utils.lifespan import lifespan

limiter = Limiter(key_func=get_remote_address)


def create_app() -> FastAPI:
    """
    App 工厂函数：负责组装所有组件
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version="1.0.0",
        redirect_slashes=False,
        docs_url=None,
        redoc_url=None,
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # 0. 注册限流
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # 1. 注册全局异常处理器
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(BusinessException, business_exception_handler)

    # 2. 注册业务路由
    app.include_router(api_v1_router, prefix="/api/v1")

    # 3. 注册文档路由 (Scalar)
    register_docs(app)

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
