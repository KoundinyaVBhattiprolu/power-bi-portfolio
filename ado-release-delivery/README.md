# ADO Release Delivery — Power BI Project Pack (.pbix build kit)

For Koundinya — BI Analyst / Power BI Developer roles.
**The flagship real-experience project in his portfolio.**

> **All data in this pack is sample / anonymised data, built from
> scratch.** Koundinya's production ADO reports are on his work
> laptop and are not in this pack. The story, the scale, the
> questions and the methods are real; the rows are synthetic.

## The real story

Koundinya built ADO ticket reporting for a large product with
**600 developers and 250 testers**. The reporting showed:

- how the team was delivering for the **next release**,
- how many **defects were fixed** and how many **bugs were created**
  on the way to that release,
- **RTE support** and **client / stakeholder support** reporting.

It was first built in **R Shiny as a web app with Jenkins and a
CI/CD pipeline**, then moved to **Power BI when the team moved to
Azure DevOps (ADO)**. See `scripts/r_shiny_to_powerbi.md` for the
migration story, including the original R Shiny shape and what
replaced each part in Power BI.

## What this pack proves (for BI roles)

- **ADO / Azure DevOps reporting** — work items, sprints, releases
- **Release management** — readiness, burndown, velocity, scope
- **Defect analytics** — bugs created vs fixed, net bug change,
  defect leakage / escape rate, open-bug backlog by severity
- **CI/CD reporting** — Jenkins → ADO Pipelines migration, build
  success rate, deployment frequency
- **Stakeholder reporting** — RTE, client and stakeholder support
  tickets, SLA breach
- **R Shiny → Power BI migration** — the same questions, a better
  delivery vehicle

## What's inside

| Folder | Contents |
|---|---|
| `data/` | 5 CSVs — see table below |
| `scripts/` | `generate_ado_data.py` (run, seeded) + `r_shiny_to_powerbi.md` |
| `dax/` | `measures.dax` — all measures, ready to paste |
| `docs/` | `BUILD_GUIDE.md` — step-by-step for the .pbix |

## Datasets (verified totals, 16 Nov 2026 — re-checked from the CSVs)

| File | Rows | What it proves |
|---|---|---|
| `ado_work_items.csv` | 8,007 work items (Jan 2025 – Nov 2026) | 2,925 User Stories, 2,685 Tasks, 2,397 Bugs |
| `sprint_dim.csv` | 52 two-week sprints, 6 releases | 49 completed, 1 in progress, 2 planned |
| `builds_deployments.csv` | 696 builds | 91.7% build success; Jenkins 90.0% vs ADO Pipelines 92.4% |
| `support_tickets.csv` | 972 tickets | RTE 364, Client 295, Stakeholder 196, Internal 117 |
| `test_runs.csv` | 400 sprint × area runs | 52,399 test cases, 92.2% pass rate |

## Verified headline numbers (check your .pbix against these)

**The next release — R26.3, due 2026-12-18 (in progress, not complete):**
- Release Readiness **61.2%** — 301 of 492 stories done, 191 still open
- Bugs created **371**, fixed **222**, open **149** (net bug change **+149**)
- Completed story points **1,570** of 2,597 planned for the release
- Test pass rate **91.3%** on 7,385 test cases in R26.3

**Overall (Jan 2025 – 16 Nov 2026):**
- Bugs created **2,397**, fixed **1,895**, open **502** (net **+502**)
- Bugs created in 2026: **1,174**, fixed in 2026: **912**
- Defect leakage (bugs found in Production): **7.0%** (167 of 2,397)
- Open bugs by severity: Critical **24**, High **121**, Medium **235**, Low **122**
- Sprint velocity: **279.1 story points** on average across the 49
  completed sprints (range 169–341)
- Past releases finished at **94.0–94.5%** story completion — the
  next release is the one with the story still to tell
- Build success **91.7%**; production deployments **97** (41 in 2026)
- Support: **81** tickets open or in progress, SLA breach **7.9%**
  (77 of 972 tickets)

## Quick start (first .pbix in ~10–15 min)

1. Open Power BI Desktop → Get Data → Text/CSV → load all 5 CSVs
   from `data/`.
2. Model view: relate `WorkItems[SprintID]` → `Sprints[SprintID]`,
   `Builds[SprintID]` → `Sprints[SprintID]`,
   `Tests[SprintID]` → `Sprints[SprintID]`. Add a Date table
   (DAX snippet at the bottom of `dax/measures.dax`) and relate
   `WorkItems[CreatedDate]` → `Date[Date]` (active) and
   `WorkItems[ClosedDate]` → `Date[Date]` (inactive).
3. Paste the measures from `dax/measures.dax`.
4. Build the 5 pages in `docs/BUILD_GUIDE.md` (Release Overview,
   Defects & Bugs, Sprint Delivery, RTE & Stakeholder Support,
   CI/CD Pipeline) and check the KPIs above.
5. Save as `06-ADO-Release-Delivery.pbix`.

To regenerate the data: `cd scripts && python3 generate_ado_data.py`
(seeded — same numbers every run).

## The interview story (use it verbatim)

> "For a product with 600 developers and 250 testers, I built the
> reporting that told us whether we would make the next release:
> stories done against scope, bugs created against bugs fixed, and
> whether defects were leaking to production. It started as an
> R Shiny web app deployed through Jenkins, and when we moved to
> Azure DevOps I rebuilt it in Power BI — same questions, but now
> the RTE, clients and stakeholders all looked at one published
> report instead of a separate portal. In this sample rebuild the
> next release, R26.3, is at 61.2% readiness with 149 bugs still
> open — that open-bug list, by severity, is the release
> conversation."

## Notes / limits (honest)

- The Python generator was run and verified here. The R code in
  `r_shiny_to_powerbi.md` is the original approach described from
  memory — it was **not run here (R is not installed on this
  machine)**.
- Sample data is scaled to the real team's size (600 devs +
  250 testers, thousands of work items), but the numbers are
  synthetic. Do not present them as production figures — present
  the *method* as the real experience.
