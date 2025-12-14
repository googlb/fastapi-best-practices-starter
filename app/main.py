# app/main.py
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from scalar_fastapi import get_scalar_api_reference,Theme, Layout
from app.api.v1.router import api_v1_router

app = FastAPI(title="Enterprise API Platform")
app.include_router(api_v1_router, prefix="/api/v1")

# ------------------------------------------------------------------
# 1. 核心工具：Schema 过滤器
# ------------------------------------------------------------------
def get_subset_openapi(tag_prefix: str, title: str, version: str):
    """
    根据 Tag 前缀过滤路由，生成独立的 OpenAPI Schema
    """
    if app.routes:
        # 逻辑：只保留 tags 列表中包含以 tag_prefix 开头的路由
        filtered_routes = [
            r for r in app.routes
            if hasattr(r, "tags") and r.tags and any(t.startswith(tag_prefix) for t in r.tags)
        ]

        return get_openapi(
            title=title,
            version=version,
            description=f"API documentation for {title}",
            routes=filtered_routes,
        )
    return {}

# ------------------------------------------------------------------
# 2. 定义 JSON 数据源端点 (隐蔽路由)
# ------------------------------------------------------------------

@app.get("/openapi/sys.json", include_in_schema=False)
async def openapi_sys():
    """生成后台管理系统的 JSON"""
    return get_subset_openapi(tag_prefix="Sys", title="System Management API", version="1.0")

@app.get("/openapi/app.json", include_in_schema=False)
async def openapi_app():
    """生成前端应用的 JSON"""
    return get_subset_openapi(tag_prefix="App", title="Client App API", version="1.0")

# ------------------------------------------------------------------
# 3. Scalar 文档聚合页 (文档中心)
# ------------------------------------------------------------------

@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        title="API Documentation Hub",

        # 【核心配置】多源下拉菜单
        sources=[
            {
                "title": "🛡️ System Management",
                "url": "/openapi/sys.json",
                "default": True
            },
            {
                "title": "📱 Client Application",
                "url": "/openapi/app.json"
            },
            {
                "title": "👁️ All Endpoints (Debug)",
                "url": "/openapi.json"
            }
        ],

        # UI 风格配置
        theme=Theme.DEFAULT,      # 推荐 purple 或 deepSpace
        layout=Layout.MODERN,     # modern 布局更适合多源文档
        hide_models=True,    # 可选：初始隐藏底部的 Models 定义，让界面更清爽
    )
