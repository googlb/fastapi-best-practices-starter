from fastapi import APIRouter

# Import routers from domains
from app.domains.news.router import router as news_router
# from app.domains.order.router import router as order_router

api_v1_router = APIRouter()

api_v1_router.include_router(news_router)
# api_v1_router.include_router(order_router)
