"""庫存相關的 Pydantic schema。"""

from pydantic import BaseModel


class LowStockItem(BaseModel):
    productid: int
    name: str
    productnumber: str
    total_quantity: int
    reorderpoint: int
    safetystocklevel: int
