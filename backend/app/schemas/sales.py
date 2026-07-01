"""銷售彙總相關的 Pydantic schema。"""

from decimal import Decimal

from pydantic import BaseModel


class CategorySales(BaseModel):
    category: str
    revenue: Decimal


class SalesSummary(BaseModel):
    month: str
    total_orders: int
    total_revenue: Decimal
    by_category: list[CategorySales]
