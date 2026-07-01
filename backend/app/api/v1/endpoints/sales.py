"""銷售彙總查詢端點。"""

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.product import Product, ProductCategory, ProductSubcategory
from app.models.sales_order import SalesOrderDetail, SalesOrderHeader
from app.schemas.sales import CategorySales, SalesSummary

router = APIRouter(prefix="/sales", tags=["sales"])


def _month_range(month: str) -> tuple[date, date]:
    try:
        year_str, mon_str = month.split("-")
        year, mon = int(year_str), int(mon_str)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail="month 格式須為 YYYY-MM") from exc
    start = date(year, mon, 1)
    end = date(year + 1, 1, 1) if mon == 12 else date(year, mon + 1, 1)
    return start, end


@router.get("/summary", response_model=SalesSummary)
def get_sales_summary(
    month: str = Query(..., description="格式為 YYYY-MM，例如 2013-05"),
    db: Session = Depends(get_db),
) -> SalesSummary:
    start, end = _month_range(month)

    order_stmt = select(
        func.count(SalesOrderHeader.salesorderid),
        func.coalesce(func.sum(SalesOrderHeader.subtotal), 0),
    ).where(SalesOrderHeader.orderdate >= start, SalesOrderHeader.orderdate < end)
    total_orders, total_revenue = db.execute(order_stmt).one()

    revenue = func.sum(
        SalesOrderDetail.unitprice
        * SalesOrderDetail.orderqty
        * (1 - SalesOrderDetail.unitpricediscount)
    ).label("revenue")
    category_stmt = (
        select(ProductCategory.name, revenue)
        .select_from(SalesOrderDetail)
        .join(
            SalesOrderHeader,
            SalesOrderHeader.salesorderid == SalesOrderDetail.salesorderid,
        )
        .join(Product, Product.productid == SalesOrderDetail.productid)
        .join(
            ProductSubcategory,
            ProductSubcategory.productsubcategoryid == Product.productsubcategoryid,
        )
        .join(
            ProductCategory,
            ProductCategory.productcategoryid == ProductSubcategory.productcategoryid,
        )
        .where(SalesOrderHeader.orderdate >= start, SalesOrderHeader.orderdate < end)
        .group_by(ProductCategory.name)
        .order_by(revenue.desc())
    )
    category_rows = db.execute(category_stmt).all()

    return SalesSummary(
        month=month,
        total_orders=total_orders,
        total_revenue=total_revenue,
        by_category=[
            CategorySales(category=row.name, revenue=row.revenue)
            for row in category_rows
        ],
    )
