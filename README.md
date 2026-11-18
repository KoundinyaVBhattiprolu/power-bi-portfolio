# Power BI Portfolio — Koundinya Bhattiprolu
📄 Resume: [Venkata Koundinya Bhattiprolu — Resume (PDF)](Venkata_Koundinya_Bhattiprolu_Resume.pdf)

BI Analyst / Power BI Developer portfolio. All projects are **sample projects with sample data, built from scratch** — my production reports live on my work laptop and are not shared here. The stories, scale, questions and methods are real; the rows are synthetic.

**Interactive portfolio site:** `docs/index.html` — the same portfolio as a single HTML page. Enable GitHub Pages (Settings → Pages → Deploy from branch `main`, folder `/docs`) and it is hosted at `https://koundinyavbhattiprolu.github.io/power-bi-portfolio/`.
**Resume:** send-ready BI resume (2 pages) — ask me for the latest copy.

## Projects

| Project | What it shows | Key sample figures |
|---|---|---|
| **ADO Release Delivery** (flagship) | Release readiness, bugs created vs fixed, test pass rate, CI/CD and stakeholder reporting for a large product — modelled on my real ADO reporting for 600 developers and 250 testers | R26.3 readiness 61.2%; 371 bugs created vs 222 fixed; test pass rate 91.3% for R26.3 vs 92.2% overall |
| **Sales Performance** | Star-schema model, time intelligence, DAX | 2025 revenue ₹4.82 Cr, +12.4% YoY, 23.6% margin |
| **Finance P&L** | Monthly P&L, budget vs actual | 2025 revenue ₹9.80 Cr, net profit ₹1.16 Cr |
| **HR Attrition** | Attrition, tenure and hiring analysis | Attrition 13.8% (171 of 1,240 employees) |
| **Supply Chain** | Inventory risk, on-time delivery | 18 SKUs at risk; 94.6% on-time delivery |
| **Messy Data → Power BI (ETL)** | Python (pandas) / R cleaning, then Power BI modelling | 1,531 messy rows → 1,433 clean rows; 0 duplicates, 0 null dates, 0 negative quantities |

## What's in this repo

- `data/` — sample CSVs for Sales, Finance, HR, Supply Chain and the messy-data ETL project
- `scripts/` — `clean_sales_python.py` (tested), `clean_sales_r.R`
- `dax/` — copy-ready DAX measures for those projects
- `docs/` — step-by-step build guides for building each `.pbix` in Power BI Desktop, plus `index.html`, the interactive portfolio site
- `ado-release-delivery/` — the flagship ADO project as its own complete pack: its own README, 5 CSVs, DAX, build guide, the seeded sample-data generator (`generate_ado_data.py`) and the R Shiny → Power BI migration note

## Build a .pbix

1. Power BI Desktop → Get Data → Text/CSV → the project's CSVs.
2. Model view: relate the fact table to the date and dimension tables; mark the date table.
3. Paste the measures from `dax/measures.dax` (or `ado-release-delivery/dax/measures.dax` for the ADO project).
4. Build the visuals in `docs/BUILD_GUIDE.md` and save as `<project>.pbix`.

Native `.pbix` files can only be created in Power BI Desktop, so they are not committed here — this repo is the complete build kit instead.

## Skills

Power BI · DAX · Data modelling (star schema) · Python (pandas) · R (dplyr) · Data wrangling / ETL · Azure DevOps reporting · Stakeholder reporting

## Notes

- The Python cleaner was run and verified; the R script follows the same logic — run it in RStudio to confirm (R was not available where this was prepared).
- The CSVs in this repo are the source of truth for every figure. Two figures on the portfolio site are still being checked against them (Finance budget accuracy and Supply Chain lead time).
