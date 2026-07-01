"""Product 查詢端點，做為資料層骨架的驗證範例。"""

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.product import Product
from app.schemas.product import ProductRead

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductRead])
def list_products(
    skip: int = 0, limit: int = 20, db: Session = Depends(get_db)
) -> list[Product]:
    stmt = select(Product).offset(skip).limit(limit)
    return list(db.scalars(stmt))
