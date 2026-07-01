"""訂單查詢端點。"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.sales_order import SalesOrderHeader
from app.schemas.order import OrderRead

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("", response_model=list[OrderRead])
def list_orders(
    customer_id: int | None = Query(default=None),
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
) -> list[SalesOrderHeader]:
    stmt = select(SalesOrderHeader).order_by(SalesOrderHeader.orderdate.desc())
    if customer_id is not None:
        stmt = stmt.where(SalesOrderHeader.customerid == customer_id)
    stmt = stmt.offset(skip).limit(limit)
    return list(db.scalars(stmt))
