"""匯入所有 model，確保 metadata 完整註冊。"""

from app.models.base import Base
from app.models.customer import BusinessEntity, Customer, Person, Store
from app.models.inventory import Location, ProductInventory
from app.models.product import Product, ProductCategory, ProductSubcategory
from app.models.sales_order import SalesOrderDetail, SalesOrderHeader

__all__ = [
    "Base",
    "BusinessEntity",
    "Person",
    "Customer",
    "Store",
    "ProductCategory",
    "ProductSubcategory",
    "Product",
    "Location",
    "ProductInventory",
    "SalesOrderHeader",
    "SalesOrderDetail",
]
