"""庫存相關資料表：production.location / productinventory。"""

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Numeric, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.product import Product


class Location(Base):
    __tablename__ = "location"
    __table_args__ = {"schema": "production"}

    locationid: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    costrate: Mapped[Decimal] = mapped_column(Numeric)
    availability: Mapped[Decimal] = mapped_column(Numeric(8, 2))
    modifieddate: Mapped[datetime]

    inventories: Mapped[list["ProductInventory"]] = relationship(
        back_populates="location"
    )


class ProductInventory(Base):
    __tablename__ = "productinventory"
    __table_args__ = {"schema": "production"}

    productid: Mapped[int] = mapped_column(
        ForeignKey("production.product.productid"), primary_key=True
    )
    locationid: Mapped[int] = mapped_column(
        SmallInteger,
        ForeignKey("production.location.locationid"),
        primary_key=True,
    )
    shelf: Mapped[str] = mapped_column(String(10))
    bin: Mapped[int] = mapped_column(SmallInteger)
    quantity: Mapped[int] = mapped_column(SmallInteger)
    modifieddate: Mapped[datetime]

    product: Mapped["Product"] = relationship(back_populates="inventories")
    location: Mapped[Location] = relationship(back_populates="inventories")
