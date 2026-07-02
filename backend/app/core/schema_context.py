"""餵給 LLM 的資料表白名單與描述，只涵蓋 Text-to-SQL 允許查詢的範圍。"""

SCHEMA_CONTEXT = """\
可用資料表（PostgreSQL，欄位名稱皆為小寫，須使用 schema 前綴）：

person.businessentity（實體基底表）
  - businessentityid (int, PK)

person.person（個人資料，對應 businessentity）
  - businessentityid (int, PK, FK -> person.businessentity.businessentityid)
  - firstname, lastname (text)

sales.store（商店，對應 businessentity）
  - businessentityid (int, PK, FK -> person.businessentity.businessentityid)
  - name (text)

sales.customer（客戶）
  - customerid (int, PK)
  - personid (int, FK -> person.person.businessentityid，個人客戶用)
  - storeid (int, FK -> sales.store.businessentityid，商店客戶用)
  - territoryid (int)

production.productcategory（產品大分類）
  - productcategoryid (int, PK)
  - name (text)

production.productsubcategory（產品子分類）
  - productsubcategoryid (int, PK)
  - productcategoryid (int, FK -> production.productcategory.productcategoryid)
  - name (text)

production.product（產品）
  - productid (int, PK)
  - name, productnumber (text)
  - productsubcategoryid (int, FK -> production.productsubcategory.productsubcategoryid)
  - safetystocklevel, reorderpoint (int)
  - standardcost, listprice (numeric)

production.location（倉儲地點）
  - locationid (int, PK)
  - name (text)

production.productinventory（產品庫存，依地點分列）
  - productid (int, FK -> production.product.productid)
  - locationid (int, FK -> production.location.locationid)
  - quantity (int)

sales.salesorderheader（銷售訂單主檔）
  - salesorderid (int, PK)
  - orderdate, duedate, shipdate (timestamp)
  - status (smallint)
  - customerid (int, FK -> sales.customer.customerid)
  - subtotal, taxamt, freight, totaldue (numeric)

sales.salesorderdetail（銷售訂單明細）
  - salesorderid (int, FK -> sales.salesorderheader.salesorderid)
  - salesorderdetailid (int)
  - productid (int, FK -> production.product.productid)
  - orderqty (smallint)
  - unitprice, unitpricediscount (numeric)
"""
