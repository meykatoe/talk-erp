"""彙整 v1 版所有路由。"""

from fastapi import APIRouter

from app.api.v1.endpoints import health, inventory, orders, products, query, sales

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(products.router)
api_router.include_router(orders.router)
api_router.include_router(inventory.router)
api_router.include_router(sales.router)
api_router.include_router(query.router)
