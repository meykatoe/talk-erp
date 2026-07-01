"""訂單相關的 Pydantic schema。"""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class OrderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    salesorderid: int
    customerid: int
    orderdate: datetime
    duedate: datetime
    shipdate: datetime | None
    status: int
    subtotal: Decimal
    taxamt: Decimal
    freight: Decimal
    totaldue: Decimal | None
