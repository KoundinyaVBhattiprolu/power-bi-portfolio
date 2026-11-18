"""
Clean messy_sales_raw.csv -> messy_sales_clean.csv
Mirrors the Python snippet in Koundinya's portfolio (pandas).
Run:  python clean_sales_python.py
Input:  ../data/messy_sales_raw.csv
Output: ../data/messy_sales_clean.csv
Fixes all 14 issues listed in ../data/messy_issues.txt
"""
import pandas as pd

df = pd.read_csv("../data/messy_sales_raw.csv", dtype=str, keep_default_na=False)

# 1. Trim whitespace everywhere
df = df.apply(lambda c: c.str.strip() if c.dtype == "object" else c)

# 2. Revenue: strip ₹ and thousands separators, then numeric (blank -> 0, as in portfolio)
df["revenue"] = (
    df["revenue"].str.replace("₹", "", regex=False)
    .str.replace(",", "", regex=False)
    .str.strip()
)
df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce").fillna(0)

# 3. Dates: mixed DD/MM/YYYY and YYYY-MM-DD.
# pd.to_datetime with a single inferred format silently drops the other
# format, so parse each format explicitly and combine them.
iso = pd.to_datetime(df["order_date"], format="%Y-%m-%d", errors="coerce")
dmy = pd.to_datetime(df["order_date"], format="%d/%m/%Y", errors="coerce")
df["order_date"] = iso.fillna(dmy)
df = df.dropna(subset=["order_date"])  # drops blank dates and 31/02/2025

# 4. Duplicates: exact duplicates + same order_id in different case
df["order_id"] = df["order_id"].str.upper()
df = df.drop_duplicates(subset=["order_id"])

# 5. Region / category standardisation
df["region"] = df["region"].str.strip().str.title()
df["category"] = df["category"].replace({"Electronic": "Electronics"})

# 6. Quantity: negative quantities are data errors -> drop those rows
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
df = df[df["quantity"] > 0]

# 7. Channel: blank -> "Unknown"
df["channel"] = df["channel"].replace("", "Unknown")

df = df.sort_values("order_date")
df.to_csv("../data/messy_sales_clean.csv", index=False)
print(f"Cleaned rows: {len(df)}  (raw file had 1,531 rows incl. 30 duplicates)")
print(df.head().to_string(index=False))
