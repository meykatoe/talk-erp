"""訂單相關資料表：sales.salesorderheader / salesorderdetail。"""

import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Numeric, SmallInteger, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.customer import Customer


class SalesOrderHeader(Base):
    __tablename__ = "salesorderheader"
    __table_args__ = {"schema": "sales"}

    salesorderid: Mapped[int] = mapped_column(primary_key=True)
    revisionnumber: Mapped[int] = mapped_column(SmallInteger)
    orderdate: Mapped[datetime]
    duedate: Mapped[datetime]
    shipdate: Mapped[datetime | None]
    status: Mapped[int] = mapped_column(SmallInteger)
    onlineorderflag: Mapped[bool]
    purchaseordernumber: Mapped[str | None] = mapped_column(String(25))
    accountnumber: Mapped[str | None] = mapped_column(String(15))
    customerid: Mapped[int] = mapped_column(ForeignKey("sales.customer.customerid"))
    salespersonid: Mapped[int | None]
    territoryid: Mapped[int | None]
    billtoaddressid: Mapped[int]
    shiptoaddressid: Mapped[int]
    shipmethodid: Mapped[int]
    subtotal: Mapped[Decimal] = mapped_column(Numeric)
    taxamt: Mapped[Decimal] = mapped_column(Numeric)
    freight: Mapped[Decimal] = mapped_column(Numeric)
    totaldue: Mapped[Decimal | None] = mapped_column(Numeric)
    comment: Mapped[str | None] = mapped_column(String(128))
    rowguid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    modifieddate: Mapped[datetime]

    customer: Mapped["Customer"] = relationship(back_populates="sales_orders")
    details: Mapped[list["SalesOrderDetail"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )


class SalesOrderDetail(Base):
    __tablename__ = "salesorderdetail"
    __table_args__ = {"schema": "sales"}

    salesorderid: Mapped[int] = mapped_column(
        ForeignKey("sales.salesorderheader.salesorderid"), primary_key=True
    )
    salesorderdetailid: Mapped[int] = mapped_column(primary_key=True)
    carriertrackingnumber: Mapped[str | None] = mapped_column(String(25))
    orderqty: Mapped[int] = mapped_column(SmallInteger)
    productid: Mapped[int] = mapped_column(ForeignKey("production.product.productid"))
    specialofferid: Mapped[int]
    unitprice: Mapped[Decimal] = mapped_column(Numeric)
    unitpricediscount: Mapped[Decimal] = mapped_column(Numeric)
    rowguid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    modifieddate: Mapped[datetime]

    order: Mapped[SalesOrderHeader] = relationship(back_populates="details")
