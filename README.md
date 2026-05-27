# Data Cleaning Project

this is project 1 from the DecodeLabs data analytics internship (batch 2026)

the idea is pretty simple — take a messy excel file and clean it up so it's actually usable for analysis later.

---

## what i worked with

the dataset has 1200 rows of e-commerce orders with 14 columns (order IDs, dates, products, prices, payment methods etc.)

---

## what i did

**missing values**
the CouponCode column had 309 empty cells. instead of just deleting those rows i filled them with "NO_COUPON" since it just means the order didn't use a coupon. learned that deleting rows is usually the wrong move

**duplicates**
checked for duplicate rows and duplicate order IDs — came back clean, nothing to remove

**dates**
converted everything to YYYY-MM-DD format (ISO 8601). all 1200 dates parsed fine with no errors

**text columns**
stripped extra spaces and applied title case on columns like Product, OrderStatus, PaymentMethod. left things like OrderID and CouponCode as-is since changing their case would break them

**prices**
rounded UnitPrice and TotalPrice to 2 decimal places

**price check**
verified that TotalPrice = Quantity x UnitPrice for every row. zero mismatches which is good

---

## results

after cleaning: 0 missing values, 0 duplicates, 0 date errors

output saved to `Dataset_Cleaned.xlsx`

---
