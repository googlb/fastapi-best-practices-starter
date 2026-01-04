# app/main.py
from fastapi import FastAPI
from app.api.v1.router import api_v1_router
from app.core.config import settings
from app.core.docs import register_docs  # 导入刚才封装的函数

def create_app() -> FastAPI:
    """
    App 工厂函数：负责组装所有组件
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version="1.0.0",
        redirect_slashes=False,  # 关闭自动重定向
        docs_url=None,    # 禁用默认 Swagger UI
        redoc_url=None,   # 禁用默认 ReDoc
        openapi_url="/openapi.json" # 保留默认的全量 JSON 源
    )

    # 1. 注册业务路由
    app.include_router(api_v1_router, prefix="/api/v1")

    # 2. 注册文档路由 (Scalar)
    # 必须在 include_router 之后注册，否则找不到路由来生成文档
    register_docs(app)

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
