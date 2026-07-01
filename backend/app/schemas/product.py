"""Product 相關的 Pydantic schema。"""

from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ProductRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    productid: int
    name: str
    productnumber: str
    listprice: Decimal
    productsubcategoryid: int | None
