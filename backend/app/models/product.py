"""產品相關資料表：production.productcategory / productsubcategory / product。"""

import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.inventory import ProductInventory


class ProductCategory(Base):
    __tablename__ = "productcategory"
    __table_args__ = {"schema": "production"}

    productcategoryid: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    rowguid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    modifieddate: Mapped[datetime]

    subcategories: Mapped[list["ProductSubcategory"]] = relationship(
        back_populates="category"
    )


class ProductSubcategory(Base):
    __tablename__ = "productsubcategory"
    __table_args__ = {"schema": "production"}

    productsubcategoryid: Mapped[int] = mapped_column(primary_key=True)
    productcategoryid: Mapped[int] = mapped_column(
        ForeignKey("production.productcategory.productcategoryid")
    )
    name: Mapped[str] = mapped_column(String(50))
    rowguid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    modifieddate: Mapped[datetime]

    category: Mapped[ProductCategory] = relationship(back_populates="subcategories")
    products: Mapped[list["Product"]] = relationship(back_populates="subcategory")


class Product(Base):
    __tablename__ = "product"
    __table_args__ = {"schema": "production"}

    productid: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    productnumber: Mapped[str] = mapped_column(String(25))
    makeflag: Mapped[bool]
    finishedgoodsflag: Mapped[bool]
    color: Mapped[str | None] = mapped_column(String(15))
    safetystocklevel: Mapped[int]
    reorderpoint: Mapped[int]
    standardcost: Mapped[Decimal] = mapped_column(Numeric)
    listprice: Mapped[Decimal] = mapped_column(Numeric)
    size: Mapped[str | None] = mapped_column(String(5))
    daystomanufacture: Mapped[int]
    productline: Mapped[str | None] = mapped_column(String(2))
    class_: Mapped[str | None] = mapped_column("class", String(2))
    style: Mapped[str | None] = mapped_column(String(2))
    productsubcategoryid: Mapped[int | None] = mapped_column(
        ForeignKey("production.productsubcategory.productsubcategoryid")
    )
    sellstartdate: Mapped[datetime]
    sellenddate: Mapped[datetime | None]
    discontinueddate: Mapped[datetime | None]
    rowguid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    modifieddate: Mapped[datetime]

    subcategory: Mapped[ProductSubcategory | None] = relationship(
        back_populates="products"
    )
    inventories: Mapped[list["ProductInventory"]] = relationship(
        back_populates="product"
    )
