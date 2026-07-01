"""客戶相關資料表：person.businessentity / person.person / sales.customer / sales.store。"""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.sales_order import SalesOrderHeader


class BusinessEntity(Base):
    """所有實體（人員、商店、供應商）共用的基底表。"""

    __tablename__ = "businessentity"
    __table_args__ = {"schema": "person"}

    businessentityid: Mapped[int] = mapped_column(primary_key=True)
    rowguid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    modifieddate: Mapped[datetime]


class Person(Base):
    __tablename__ = "person"
    __table_args__ = {"schema": "person"}

    businessentityid: Mapped[int] = mapped_column(
        ForeignKey("person.businessentity.businessentityid"), primary_key=True
    )
    persontype: Mapped[str] = mapped_column(String(2))
    namestyle: Mapped[bool]
    title: Mapped[str | None] = mapped_column(String(8))
    firstname: Mapped[str] = mapped_column(String(50))
    middlename: Mapped[str | None] = mapped_column(String(50))
    lastname: Mapped[str] = mapped_column(String(50))
    suffix: Mapped[str | None] = mapped_column(String(10))
    emailpromotion: Mapped[int]
    rowguid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    modifieddate: Mapped[datetime]

    customer: Mapped["Customer | None"] = relationship(back_populates="person")


class Store(Base):
    __tablename__ = "store"
    __table_args__ = {"schema": "sales"}

    businessentityid: Mapped[int] = mapped_column(
        ForeignKey("person.businessentity.businessentityid"), primary_key=True
    )
    name: Mapped[str] = mapped_column(String(50))
    salespersonid: Mapped[int | None]
    rowguid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    modifieddate: Mapped[datetime]

    customers: Mapped[list["Customer"]] = relationship(back_populates="store")


class Customer(Base):
    __tablename__ = "customer"
    __table_args__ = {"schema": "sales"}

    customerid: Mapped[int] = mapped_column(primary_key=True)
    personid: Mapped[int | None] = mapped_column(
        ForeignKey("person.person.businessentityid")
    )
    storeid: Mapped[int | None] = mapped_column(
        ForeignKey("sales.store.businessentityid")
    )
    territoryid: Mapped[int | None]
    rowguid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    modifieddate: Mapped[datetime]

    person: Mapped[Person | None] = relationship(back_populates="customer")
    store: Mapped[Store | None] = relationship(back_populates="customers")
    sales_orders: Mapped[list["SalesOrderHeader"]] = relationship(
        back_populates="customer"
    )
