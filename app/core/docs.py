# app/core/docs.py
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from scalar_fastapi import get_scalar_api_reference, Layout, Theme
try:
    # 1. 正常人的逻辑：直接导入
    from scalar_fastapi import OpenAPISource
except ImportError:
    # 2. 我们的逻辑：官方没导出来？我自己去深层目录找！
    from scalar_fastapi.scalar_fastapi import OpenAPISource

def custom_openapi(app: FastAPI, tag_prefix: str, title: str, version: str):
    """
    辅助函数：根据 Tag 前缀过滤路由，生成独立的 OpenAPI Schema
    """
    if app.routes:
        filtered_routes = [
            r for r in app.routes
            if hasattr(r, "tags") and r.tags and any(t.startswith(tag_prefix) for t in r.tags)
        ]
        return get_openapi(
            title=title,
            version=version,
            description=f"{title} - 接口文档",
            routes=filtered_routes,
        )
    return {}

def register_docs(app: FastAPI):
    """
    核心函数：在 App 上注册文档路由
    """

    # 1. 定义 JSON 数据源 (隐蔽路由)
    @app.get("/openapi/sys.json", include_in_schema=False)
    async def openapi_sys():
        return custom_openapi(app, tag_prefix="Sys", title="🛡️ 后台管理系统 API", version="1.0")

    @app.get("/openapi/app.json", include_in_schema=False)
    async def openapi_app():
        return custom_openapi(app, tag_prefix="App", title="📱 客户端应用 API", version="1.0")

    # 2. 定义 Scalar 文档入口 (覆盖 /docs)
    @app.get("/docs", include_in_schema=False)
    async def scalar_html():
        return get_scalar_api_reference(
            title="API Documentation Hub",
            layout=Layout.MODERN,
            theme=Theme.PURPLE,
            hide_models=True, # 默认隐藏底部的 Models 区域，界面更清爽

            # 【关键修正】这里必须用 sources 才能实现下拉菜单切换！
            # 不要传 openapi_url="/openapi.json"，否则下面这些配置都不生效
            sources=[
                OpenAPISource(
                    title="🛡️ 后台管理 (System)",
                    url="/openapi/sys.json",
                    default=True
                ),
                OpenAPISource(
                    title="📱 客户端 (App)",
                    url="/openapi/app.json"
                ),
                OpenAPISource(
                    title="👁️ 全量接口 (Debug)",
                    url="/openapi.json"
                )
            ]
        )
