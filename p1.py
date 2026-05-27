import pandas as pd
import numpy as np

INPUT_FILE = "Dataset for Data Analytics.xlsx"
OUTPUT_FILE = "Dataset_Cleaned.xlsx"

data = pd.read_excel(INPUT_FILE)

# quick look at what we have
print("Initial overview")
print("rows:", data.shape[0])
print("cols:", data.shape[1])
print("columns:", list(data.columns))
print()

# --- missing values ---
print("Checking missing values...")
nans = data.isnull().sum()
print("Before:")
print(nans[nans > 0])
print()

data["CouponCode"] = data["CouponCode"].fillna("NO_COUPON")

remaining = data.isnull().sum().sum()
print(f"After cleanup: {remaining} missing values left")
print("filled CouponCode blanks with NO_COUPON\n")

# --- duplicates ---
print("Duplicates check")
full_dups = data.duplicated().sum()
order_dups = data["OrderID"].duplicated().sum()

print("duplicate rows:", full_dups)
print("duplicate OrderIDs:", order_dups)

if full_dups > 0:
    data = data.drop_duplicates()
    print(f"dropped {full_dups} rows")
else:
    print("nothing to drop here")

if order_dups > 0:
    data = data.drop_duplicates(subset="OrderID")
    print(f"dropped {order_dups} duplicate order IDs\n")
else:
    print("order IDs look clean\n")

# --- fix dates ---
print("Fixing date format...")
data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
bad_dates = data["Date"].isnull().sum()
data["Date"] = data["Date"].dt.strftime('%Y-%m-%d')

print("converted to YYYY-MM-DD")
if bad_dates > 0:
    print(f"warning: {bad_dates} dates couldn't be parsed\n")
else:
    print("all dates look fine\n")

# --- text cleanup ---
print("Cleaning text columns...")

cols_to_clean = [
    "Product", "OrderStatus", "PaymentMethod",
    "ReferralSource", "CouponCode", "CustomerID",
    "ShippingAddress", "TrackingNumber"
]

skip_titlecase = ["CouponCode", "CustomerID", "TrackingNumber"]

for col in cols_to_clean:
    if col not in data.columns:
        continue
    data[col] = data[col].astype(str).str.strip()
    if col not in skip_titlecase:
        data[col] = data[col].str.title()

print("stripped spaces and applied title case where needed\n")

# --- round numbers ---
print("Rounding prices...")
data["UnitPrice"] = data["UnitPrice"].round(2)
data["TotalPrice"] = data["TotalPrice"].round(2)
print("done\n")

# --- check totals make sense ---
print("Verifying TotalPrice...")
expected = (data["Quantity"] * data["UnitPrice"]).round(2)
bad = (data["TotalPrice"] != expected).sum()

print(f"mismatches found: {bad}")
if bad == 0:
    print("all good\n")
else:
    print(f"heads up: {bad} rows have inconsistent totals\n")

# --- final summary ---
print("Final state:")
print("rows          :", data.shape[0])
print("cols          :", data.shape[1])
print("missing       :", data.isnull().sum().sum())
print("duplicates    :", data.duplicated().sum())
print("dup order IDs :", data["OrderID"].duplicated().sum())
print("bad dates     :", data["Date"].isnull().sum())
print()

data.to_excel(OUTPUT_FILE, index=False)
print("saved to", OUTPUT_FILE)
