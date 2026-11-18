# Build guide — 5 .pbix files from this pack

Power BI Desktop only (free). Each project is one .pbix. Do them in order;
project 1 teaches the pattern the others repeat.

## Common setup (every project)

1. Home → Get Data → Text/CSV → pick the files listed for that project.
2. In Power Query, check types: dates as Date, money as Decimal Number,
   IDs as Text. Close & Apply.
3. Model view → create the relationships listed. Single direction, star schema.
4. Modeling → New measure → paste from `dax/measures.dax`.
5. Mark the date table: right-click `Date` → Mark as date table → `Date[Date]`.
   Without this, `SAMEPERIODLASTYEAR` will not work.

---

## 1. Sales Performance Dashboard → `01-Sales-Performance.pbix`

**Files:** `sales_fact.csv`, `date_dim.csv`, `product_dim.csv`
**Relationships:** `sales_fact[OrderDate]` → `Date[Date]`;
`sales_fact[ProductID]` → `product_dim[ProductID]`
**Measures:** Total Revenue, Total Cost, Profit, Profit Margin %,
Total Orders, Avg Order Value, Revenue LY, Revenue YoY %
**Expected KPIs (check yours match):** Revenue ₹4.82 Cr (2025),
18,240 orders, +12.4% YoY, 23.6% margin.
**Visuals:** KPI cards (Revenue / Orders / Margin / Returns proxy — use
Profit Margin %); slicers for Region and Channel; clustered bar —
Revenue by Category; donut — Revenue by Channel (Online 52% / Retail 30% /
Partner 18%); line — Revenue by Month; drill-through page:
Region → Product (right-click a bar → Drill through).

## 2. Messy Data → Clean Power BI Model → `02-Messy-Data-ETL.pbix`

**Files:** `messy_sales_raw.csv` (before), `messy_sales_clean.csv` (after)
**Steps:**
1. In a terminal: `cd scripts && python clean_sales_python.py`
   (or run `clean_sales_r.R` in RStudio — same result).
   Verified here: 1,531 rows in → 1,433 clean rows out.
2. Load both CSVs into Power BI. Build a small "before / after" page:
   card visuals for row counts, a table of the 14 issues from
   `data/messy_issues.txt`, and a bar of rows removed by cause
   (blank dates 52, duplicates 30, negative quantities, invalid date 1).
3. Then load `messy_sales_clean.csv` as a fact table, relate it to
   `date_dim.csv`, and reuse the Sales measures — this is the pipeline
   feeding project 1.
**Interview line:** "I don't wait for clean data — I build the cleaning
pipeline, document the 14 issues, and automate it."

## 3. Finance P&L & Budget vs Actuals → `03-Finance-PL.pbix`

**Files:** `finance_pl_monthly.csv`, `date_dim.csv`
**Relationships:** convert `finance_pl_monthly[Month]` ("2025-01") to a date
(first of the month, in Power Query: Add Column → Date → Year/Month, or
`Date.FromText([Month] & "-01")`) → `Date[Date]`.
**Measures:** Actual, Budget, Budget Variance %, Net Profit, Total COGS.
**Expected KPIs:** Revenue ₹9.80 Cr, Net Profit ₹1.16 Cr.
**Visuals:** waterfall — Revenue → COGS → Opex → Logistics → Net Profit;
line — Actual vs Budget by month; matrix — P&L by month with conditional
formatting on variance; KPI cards for Net Profit and Budget Variance %.

## 4. HR Attrition & Workforce Dashboard → `04-HR-Attrition.pbix`

**Files:** `hr_employees.csv`
**Measures:** Headcount, Employees Left, Attrition Rate %, Avg Tenure Years.
**Expected KPIs:** Headcount 1,240, Attrition 13.8%, (time-to-hire 42 days
is a portfolio figure — add it as a text KPI if asked, it is not in the CSV).
**Visuals:** KPI cards; bar — Attrition Rate % by Department; bar —
Attrition by Tenure band (create a Tenure Band column: <1 yr, 1–3, 3–5, 5+);
decomposition tree — LeftCompany by Department → Level → Location;
donut — Headcount by Department.
**Insight to surface:** attrition concentrates in the first 12 months —
pointing to onboarding, not pay.

## 5. Supply Chain & Inventory Dashboard → `05-Supply-Chain.pbix`

**Files:** `supply_inventory.csv`, `supply_shipments.csv`
**Relationships:** `supply_shipments[SKUID]` → `supply_inventory[SKUID]`.
**Measures:** SKUs at Risk, On-Time Delivery %, Avg Lead Time Days.
**Expected KPIs:** On-time 94.6%, 18 SKUs at risk, avg lead time ~6.6 days.
**Visuals:** KPI cards; table — SKUs sorted by DaysOfCover ascending,
conditional formatting red under 7 days; bar — On-Time Delivery % by
Supplier; bar — Avg Lead Time by Supplier; map / bar — Shipments by
Destination.

---

## Publishing (optional, after the .pbix files work)

1. In Power BI Desktop: File → Publish → your Power BI workspace.
2. Or keep it local: the .pbix files themselves are the demo — open one live
   in an interview and use the slicers.
3. Add the project names + the three headline KPIs from each file to the
   resume (the resume is the next step after this pack — see README).
