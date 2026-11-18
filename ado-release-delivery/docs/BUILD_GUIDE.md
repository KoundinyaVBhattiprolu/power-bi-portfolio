# Build guide — ADO Release Delivery → `06-ADO-Release-Delivery.pbix`

Power BI Desktop only (free). One .pbix, five pages. This is the
flagship project: it is the rebuild of Koundinya's real ADO reporting
(sample data — see README.md), so build it carefully and demo it live.

## Common setup

1. Home → Get Data → Text/CSV → load all 5 files from `data/`:
   `ado_work_items.csv`, `sprint_dim.csv`, `builds_deployments.csv`,
   `support_tickets.csv`, `test_runs.csv`. Rename the tables in
   Power Query to `WorkItems`, `Sprints`, `Builds`, `Support`,
   `Tests` (the DAX in `dax/measures.dax` uses these names).
2. In Power Query, check types: dates as Date, StoryPoints /
   TestCases* / DurationMinutes as Whole Number, IDs as Text.
   `ClosedDate` is blank for open items — that is correct, do not
   fill it. Close & Apply.
3. Create the Date table: Modeling → New table → paste the `Date =`
   DAX at the bottom of `dax/measures.dax`. Mark it as a date table
   (right-click `Date` → Mark as date table → `Date[Date]`).
4. Model view → create the relationships (single direction,
   star schema around Sprints + Date):
   - `WorkItems[SprintID]` → `Sprints[SprintID]`
   - `Builds[SprintID]` → `Sprints[SprintID]`
   - `Tests[SprintID]` → `Sprints[SprintID]`
   - `WorkItems[CreatedDate]` → `Date[Date]` (active)
   - `WorkItems[ClosedDate]` → `Date[Date]` (inactive — used by
     `Bugs Fixed in Period` via USERELATIONSHIP)
   - `Builds[BuildDate]` → `Date[Date]` (active)
   - `Support[CreatedDate]` → `Date[Date]` (active)
   - `Sprints[Release]` is a text column — use it as a slicer, not
     a relationship.
5. Modeling → New measure → paste all measures from
   `dax/measures.dax`.
6. Add slicers to every page: Release, SprintID, Team, Area.

**Expected KPIs — check yours match (verified from the CSVs):**
Release Readiness (R26.3) 61.2% · Test Pass Rate in R26.3 91.3%
(7,385 cases) · Bugs (overall) 2,397 created / 1,895 fixed /
502 open · Defect Leakage (overall) 7.0% · Test Pass Rate
(overall) 92.2% (52,399 cases) · Build Success (overall) 91.7% ·
SLA Breach (overall) 7.9% · Velocity 279.1 pts/sprint (average
across the 49 completed sprints).

---

## Page 1 — Release Overview

**Purpose:** the one page a release manager opens first.
**Slicers:** Release (default: R26.3), Team, Area.
**KPI cards:** Release Readiness %, Stories Completed / Total Stories,
Open Stories, Open Bugs, Net Bug Change.
**Visuals:**
- Gauge or KPI — Release Readiness % vs 100% target (R26.3: 61.2%).
- Bar — Stories Completed % by Release (past releases 94.0–94.5%,
  R26.3 61.2% — the gap is the story: the release is in progress).
- Line — Bugs Created vs Bugs Fixed by month (use CreatedDate for
  created, `Bugs Fixed in Period` for fixed; they cross when the
  team is winning).
- Table — next release scope: stories by Team with State.
**Talking point:** "61.2% with five weeks to go, and 191 stories
still open — here is exactly which teams hold them."

## Page 2 — Defects & Bugs

**Purpose:** are we winning against bugs?
**KPI cards:** Bugs Created, Bugs Fixed, Net Bug Change, Open Bugs,
Open Critical Bugs, Defect Leakage %.
**Visuals:**
- Line (bug burndown) — `Bugs Created in Period` vs
  `Bugs Fixed in Period` by month. The gap between the lines is the
  backlog growing or shrinking.
- Bar — Open Bugs by Severity (Critical 24, High 121, Medium 235,
  Low 122 — check yours match).
- Bar — Bugs Created by Root Cause; bar — Bugs by FoundIn
  (Development / Testing / UAT / Production).
- Donut — Defect Leakage: Production-found bugs 167 of 2,397 (7.0%).
- Matrix — Bugs Created vs Fixed by Release (R26.3: 371 created,
  222 fixed, 149 open).
**Talking point:** "Bugs created in 2026: 1,174. Fixed: 912.
Net +262 for the year so far — the backlog is growing, and the
leakage rate tells us whether customers feel it."

## Page 3 — Sprint Delivery

**Purpose:** velocity and predictability, sprint by sprint.
**KPI cards:** Avg Sprint Velocity, Completed Story Points,
Stories Completed %.
**Visuals:**
- Line + bar — Sprint Velocity (completed story points) by SprintID,
  with PlannedStoryPoints as a reference line. Verified average
  across the 49 completed sprints: 279.1 points (range 169–341).
- Bar — Completed Story Points by Team.
- Table — Sprints with Status (49 Completed, 1 In Progress
  — Sprint 2026-24, 16–29 Nov 2026 — 2 Planned).
- Card — current sprint: Sprint 2026-24, 54 stories, 28 done.
**Talking point:** "Velocity is stable around 279 points. The
current sprint is mid-flight — that is normal, not a delay."

## Page 4 — RTE & Stakeholder Support

**Purpose:** the reporting RTE, clients and stakeholders actually read.
**KPI cards:** Support Tickets Total (972), Support Tickets Open (81),
SLA Breach % (7.9%).
**Visuals:**
- Bar — Tickets by Source: RTE Support 364, Client 295,
  Stakeholder 196, Internal 117.
- Bar — SLA Breach % by Source (RTE has the most breaches in
  absolute terms — 35 of 77 — say so, and say why: it is also the
  largest source).
- Bar — Tickets by Priority (P0 34, P1 183, P2 454, P3 301) and by
  Category.
- Line — Tickets created by month, with open tickets highlighted.
- Table — open tickets by Source and Priority (Client: 32 open —
  the stakeholder follow-up list).
**Talking point:** "This is the page I built for the RTE and for
clients — same data as engineering, cut for the people who have to
answer for it."

## Page 5 — CI/CD Pipeline

**Purpose:** the Jenkins → ADO migration, told with build data.
**KPI cards:** Build Success Rate % (91.7%), Failed Builds (50),
Deployment Frequency (97 prod deployments, 41 in 2026).
**Visuals:**
- Bar — Build Success Rate % by Pipeline: Jenkins 90.0% vs
  ADO Pipelines 92.4%. This is the migration payoff, in one chart.
- Line — Builds per sprint, coloured by Status (Success / Failed /
  Cancelled).
- Bar — Deployments by DeploymentEnv (Dev / QA / Staging / Prod).
- Card + line — Deployment Frequency by month (prod deployments).
**Talking point:** "We moved the pipeline to ADO at the same time
as the reporting. Build success went from 90.0% on Jenkins to
92.4% on ADO Pipelines — and the reporting moved with it, so
nobody lost their view of the release."

---

## Publishing (optional, after the .pbix works)

1. In Power BI Desktop: File → Publish → your Power BI workspace.
2. Or keep it local: the .pbix itself is the demo — open it live in
   an interview, set the Release slicer to R26.3, and walk pages
   1 → 2 → 5 in that order (readiness, bugs, pipeline).
3. Add to the resume / portfolio: "ADO Release Delivery dashboard —
   8,007 work items, 52 sprints, release readiness, defect leakage
   and CI/CD reporting for a 600-developer product; migrated from
   R Shiny + Jenkins to Power BI + Azure DevOps."
