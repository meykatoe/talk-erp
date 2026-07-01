"""庫存查詢端點。"""

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.inventory import ProductInventory
from app.models.product import Product
from app.schemas.inventory import LowStockItem

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.get("/low-stock", response_model=list[LowStockItem])
def list_low_stock(
    limit: int = 20,
    db: Session = Depends(get_db),
) -> list[LowStockItem]:
    total_quantity = func.sum(ProductInventory.quantity).label("total_quantity")
    stmt = (
        select(
            Product.productid,
            Product.name,
            Product.productnumber,
            Product.reorderpoint,
            Product.safetystocklevel,
            total_quantity,
        )
        .join(ProductInventory, ProductInventory.productid == Product.productid)
        .group_by(Product.productid)
        .having(total_quantity <= Product.reorderpoint)
        .order_by(total_quantity)
        .limit(limit)
    )
    rows = db.execute(stmt).all()
    return [
        LowStockItem(
            productid=row.productid,
            name=row.name,
            productnumber=row.productnumber,
            total_quantity=row.total_quantity,
            reorderpoint=row.reorderpoint,
            safetystocklevel=row.safetystocklevel,
        )
        for row in rows
    ]
