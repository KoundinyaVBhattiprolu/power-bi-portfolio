#!/usr/bin/env python3
"""
Generate sample / anonymised Azure DevOps release-delivery data for
Koundinya's Power BI portfolio project.

REAL STORY (sample data only):
  Koundinya built ADO ticket reporting for a large product with
  600 developers and 250 testers. The reporting showed how the team
  was delivering for the next release, how many defects were fixed
  and how many bugs were created on the way to that release, and
  covered RTE support and client / stakeholder support reporting.
  It was first built in R Shiny as a web app with Jenkins and a
  CI/CD pipeline, then moved to Power BI when the team moved to
  Azure DevOps (ADO).

  Production data is on his work laptop and is NOT in this pack.
  Everything generated here is synthetic, anonymised sample data
  at a plausible scale for that team (thousands of work items,
  not tens), with dates Jan 2025 - Nov 2026 and the next release
  (R26.3, due 2026-12-18) still in progress.

Outputs (in ../data/):
  ado_work_items.csv       - User Stories, Tasks, Bugs
  sprint_dim.csv           - 46 two-week sprints, 6 releases
  builds_deployments.csv   - CI/CD builds: Jenkins (early) -> ADO Pipelines
  support_tickets.csv      - RTE / client / stakeholder support tickets
  test_runs.csv            - test execution per sprint x area

Run:  python3 generate_ado_data.py
Seeded (random.seed(42)) so the numbers are reproducible.
"""
import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data"
DATA.mkdir(parents=True, exist_ok=True)

TODAY = date(2026, 11, 16)          # "today" for this pack
NEXT_RELEASE_DUE = date(2026, 12, 18)

TEAMS = [
    ("Core Platform", "Platform"),
    ("Payments", "Payments"),
    ("Search & Discovery", "Search"),
    ("Web Experience", "Web"),
    ("Mobile Apps", "Mobile"),
    ("API & Integrations", "API"),
    ("Data & Reporting", "Data"),
    ("Security & Compliance", "Security"),
    ("Checkout", "Payments"),
    ("Customer Experience", "Web"),
    ("Infrastructure", "Platform"),
    ("AI Features", "Data"),
]
AREAS = sorted({a for _, a in TEAMS})

# ---------------------------------------------------------------- sprints
# 2-week sprints, Mondays. 2025: 24 sprints, 2026: 22 sprints to mid-Nov.
# Releases: R25.1 / R25.2 / R25.3 / R26.1 / R26.2 / R26.3 (NEXT, in progress)
RELEASES = [
    ("R25.1", date(2025, 1, 6), date(2025, 4, 25)),
    ("R25.2", date(2025, 4, 28), date(2025, 8, 22)),
    ("R25.3", date(2025, 8, 25), date(2025, 12, 19)),
    ("R26.1", date(2026, 1, 5), date(2026, 4, 24)),
    ("R26.2", date(2026, 4, 27), date(2026, 8, 21)),
    ("R26.3", date(2026, 8, 24), date(2026, 12, 18)),  # NEXT RELEASE
]

sprints = []
sprint_no = 0
year_counter = {2025: 0, 2026: 0}  # SprintID must be unique per year
for rel, rel_start, rel_end in RELEASES:
    start = rel_start
    idx = 1
    while start <= rel_end and start <= TODAY + timedelta(days=35):
        end = start + timedelta(days=13)
        sprint_no += 1
        year_counter[start.year] += 1
        sid = f"{start.year}-{year_counter[start.year]:02d}"
        # status: completed if ended before today, in progress if it
        # straddles today, planned if it starts after today
        if end < TODAY:
            status = "Completed"
        elif start <= TODAY <= end:
            status = "In Progress"
        else:
            status = "Planned"
        sprints.append({
            "SprintID": sid,
            "SprintName": f"Sprint {sid}",
            "Release": rel,
            "StartDate": start,
            "EndDate": min(end, rel_end) if end > rel_end else end,
            "Status": status,
        })
        start = end + timedelta(days=1)
        idx += 1
        if start > rel_end:
            break

# Planned capacity: ~12 teams x ~25 pts = ~300 pts per sprint
for s in sprints:
    s["PlannedStoryPoints"] = random.randint(270, 330)

with open(DATA / "sprint_dim.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=[
        "SprintID", "SprintName", "Release", "StartDate", "EndDate",
        "Status", "PlannedStoryPoints"])
    w.writeheader()
    for s in sprints:
        w.writerow({**s, "StartDate": s["StartDate"].isoformat(),
                    "EndDate": s["EndDate"].isoformat()})

# ---------------------------------------------------------------- work items
STORY_TITLES = [
    "Checkout flow", "Search relevance", "Payment retry", "Mobile onboarding",
    "API rate limiting", "Dashboard performance", "User permissions",
    "Notification preferences", "Data export", "Single sign-on",
    "Order tracking", "Refund workflow", "Catalogue search", "Audit logging",
    "Accessibility fixes", "Offline mode", "Recommendation engine",
    "Bulk upload", "Two-factor auth", "Reporting export",
]
BUG_TITLES = [
    "Checkout timeout", "Search returns stale results", "Payment double-charge",
    "Mobile crash on login", "API 500 on large payload", "Dashboard slow load",
    "Permissions leak", "Notification duplicate", "Export truncates rows",
    "SSO token expiry", "Tracking status stuck", "Refund amount mismatch",
    "Filter resets on refresh", "Audit log missing entries",
    "Offline sync conflict", "Recommendation stale", "Upload fails on CSV",
    "2FA code not delivered", "Report export blank", "Session timeout too short",
]
TASK_TITLES = [
    "Refactor service", "Add unit tests", "Update documentation",
    "Database index", "Code review", "Performance profiling",
    "Security patch", "Dependency upgrade", "Monitoring alert",
    "Load test", "Fix flaky test", "Clean up tech debt",
]
ROOT_CAUSES = ["Logic error", "Regression", "Integration", "Data issue",
               "UI defect", "Performance", "Configuration", "Requirements gap"]
FOUND_IN = ["Development", "Testing", "UAT", "Production"]

work_items = []
wid = 10000

def rand_date(a: date, b: date) -> date:
    if b < a:
        return a
    return a + timedelta(days=random.randint(0, (b - a).days))

for s in sprints:
    is_next_release = s["Release"] == "R26.3"
    is_current = s["Status"] == "In Progress"
    is_planned = s["Status"] == "Planned"
    # Volume per sprint: stories ~52-60, tasks ~48-56, bugs ~42-52
    n_stories = random.randint(52, 60)
    n_tasks = random.randint(48, 56)
    n_bugs = random.randint(42, 52)
    if is_planned:
        # Planned sprints: scope is known, almost nothing is closed yet
        n_stories, n_tasks, n_bugs = (random.randint(48, 55),
                                      random.randint(40, 48),
                                      random.randint(18, 26))

    def closure_prob(kind: str) -> float:
        """Probability an item is Closed (vs still open)."""
        if is_planned:
            return 0.05
        if is_current:
            return 0.55 if kind != "Bug" else 0.45
        if is_next_release:
            # R26.3 sprints already finished: good but not complete
            return 0.82 if kind != "Bug" else 0.68
        # Completed releases: high closure
        return 0.94 if kind != "Bug" else 0.83

    def make_item(kind: str):
        global wid
        wid += 1
        team, area = random.choice(TEAMS)
        created = rand_date(s["StartDate"], min(s["EndDate"], TODAY))
        # Bugs found later in the sprint / shortly after are common
        if kind == "Bug" and random.random() < 0.3:
            created = rand_date(s["StartDate"], min(s["EndDate"] + timedelta(days=7), TODAY))
        # Planned sprints start after today: their backlog items were
        # created during grooming, not in the future.
        if created > TODAY:
            created = rand_date(TODAY - timedelta(days=30), TODAY)
        closed = None
        state = "New"
        r = random.random()
        # p_done is the total share done (Closed + Resolved); the old
        # code added Resolved on top of it, which made past releases
        # 100% done. Split p_done into Closed (85%) / Resolved (15%).
        p_done = closure_prob(kind)
        if r < p_done * 0.85:
            state = "Closed"
            closed = rand_date(created, min(created + timedelta(days=random.randint(3, 35)), TODAY))
            if closed > TODAY:
                closed = TODAY
        elif r < p_done:
            state = "Resolved"
            closed = rand_date(created, min(created + timedelta(days=random.randint(3, 28)), TODAY))
        elif r < p_done + 0.12:
            state = "Active"
        else:
            state = "New"
        if closed is not None and closed < created:
            closed = created
        title_pool = {"User Story": STORY_TITLES, "Task": TASK_TITLES, "Bug": BUG_TITLES}[kind]
        title = f"{kind}: {random.choice(title_pool)} — {area} ({team})"
        row = {
            "WorkItemID": f"ADO-{wid}",
            "WorkItemType": kind,
            "Title": title,
            "Team": team,
            "Area": area,
            "Priority": random.choices(["P0", "P1", "P2", "P3"], weights=[4, 22, 44, 30])[0],
            "Severity": (random.choices(["Critical", "High", "Medium", "Low"],
                                        weights=[6, 24, 45, 25])[0] if kind == "Bug" else ""),
            "State": state,
            "SprintID": s["SprintID"],
            "Release": s["Release"],
            "CreatedDate": created.isoformat(),
            "ClosedDate": closed.isoformat() if closed else "",
            "StoryPoints": (random.choice([1, 2, 3, 5, 8, 13]) if kind == "User Story"
                            else (random.choice([1, 2, 3, 5]) if kind == "Task" else "")),
            "FoundIn": (random.choices(FOUND_IN, weights=[38, 42, 14, 6])[0] if kind == "Bug" else ""),
            "RootCause": (random.choice(ROOT_CAUSES) if kind == "Bug" else ""),
        }
        return row

    for _ in range(n_stories):
        work_items.append(make_item("User Story"))
    for _ in range(n_tasks):
        work_items.append(make_item("Task"))
    for _ in range(n_bugs):
        work_items.append(make_item("Bug"))

with open(DATA / "ado_work_items.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(work_items[0].keys()))
    w.writeheader()
    w.writerows(work_items)

# ---------------------------------------------------------------- builds
builds = []
bid = 5000
for s in sprints:
    if s["Status"] == "Planned":
        continue
    n = random.randint(12, 16)
    for _ in range(n):
        bid += 1
        # Jenkins until Jul 2025, ADO Pipelines from Aug 2025 (the migration)
        pipeline = "Jenkins" if s["StartDate"] < date(2025, 8, 1) else "ADO Pipelines"
        # ADO is a little more reliable in this sample
        success_p = 0.88 if pipeline == "Jenkins" else 0.93
        r = random.random()
        status = "Success" if r < success_p else ("Failed" if r < success_p + 0.08 else "Cancelled")
        env = random.choices(["Dev", "QA", "Staging", "Prod"], weights=[35, 30, 20, 15])[0]
        builds.append({
            "BuildID": f"BLD-{bid}",
            "Pipeline": pipeline,
            "BuildDate": rand_date(s["StartDate"], min(s["EndDate"], TODAY)).isoformat(),
            "SprintID": s["SprintID"],
            "Release": s["Release"],
            "Branch": random.choice(["main", "main", "release/R26.3", "feature/*"]),
            "Status": status,
            "DurationMinutes": random.randint(6, 48),
            "DeploymentEnv": env,
            "Deployed": "Yes" if (status == "Success" and random.random() < 0.85) else "No",
        })

with open(DATA / "builds_deployments.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(builds[0].keys()))
    w.writeheader()
    w.writerows(builds)

# ---------------------------------------------------------------- support tickets
tickets = []
tid = 8000
SOURCES = [("RTE Support", 34), ("Client", 32), ("Stakeholder", 22), ("Internal", 12)]
CATEGORIES = ["Release query", "Defect report", "Feature request", "Performance",
              "Access / permissions", "Data issue", "Deployment query", "Training"]
start = date(2025, 1, 1)
day = start
while day <= TODAY:
    # ~1-3 tickets a day, a little heavier around release dates
    for _ in range(random.choices([0, 1, 2, 3], weights=[12, 42, 32, 14])[0]):
        tid += 1
        source = random.choices([s for s, _ in SOURCES], weights=[w for _, w in SOURCES])[0]
        priority = random.choices(["P0", "P1", "P2", "P3"], weights=[3, 18, 47, 32])[0]
        sla_hours = {"P0": 4, "P1": 8, "P2": 24, "P3": 72}[priority]
        # Older tickets mostly closed; recent ones often still open
        age_days = (TODAY - day).days
        closed_p = 0.94 if age_days > 30 else (0.78 if age_days > 7 else 0.45)
        closed = None
        status = "Open"
        if random.random() < closed_p:
            status = random.choices(["Resolved", "Closed"], weights=[35, 65])[0]
            closed = rand_date(day, min(day + timedelta(days=random.randint(1, 10)), TODAY))
        elif random.random() < 0.5:
            status = "In Progress"
        # SLA breach: more likely for P0/P1 and for open tickets
        breach_p = 0.14 if priority in ("P0", "P1") else 0.06
        if status == "Open":
            breach_p += 0.03
        tickets.append({
            "TicketID": f"SUP-{tid}",
            "CreatedDate": day.isoformat(),
            "ClosedDate": closed.isoformat() if closed else "",
            "Source": source,
            "Category": random.choice(CATEGORIES),
            "Priority": priority,
            "Status": status,
            "SLAHours": sla_hours,
            "SLABreached": "Yes" if random.random() < breach_p else "No",
            "Release": random.choice(["R25.1", "R25.2", "R25.3", "R26.1", "R26.2", "R26.3"]),
        })
    day += timedelta(days=1)

with open(DATA / "support_tickets.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(tickets[0].keys()))
    w.writeheader()
    w.writerows(tickets)

# ---------------------------------------------------------------- test runs
test_runs = []
for s in sprints:
    if s["Status"] == "Planned":
        continue
    for area in AREAS:
        executed = random.randint(95, 165)
        # Pass rate ~91-95%, a touch lower in the current / next release
        pass_rate = random.uniform(0.905, 0.95)
        if s["Release"] == "R26.3":
            pass_rate = random.uniform(0.89, 0.94)
        passed = int(executed * pass_rate)
        failed = int((executed - passed) * random.uniform(0.55, 0.75))
        blocked = executed - passed - failed
        test_runs.append({
            "SprintID": s["SprintID"],
            "Release": s["Release"],
            "Area": area,
            "TestCasesExecuted": executed,
            "TestCasesPassed": passed,
            "TestCasesFailed": failed,
            "TestCasesBlocked": blocked,
        })

with open(DATA / "test_runs.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(test_runs[0].keys()))
    w.writeheader()
    w.writerows(test_runs)

print(f"sprints: {len(sprints)}  (completed/in-progress/planned: "
      f"{sum(1 for s in sprints if s['Status']=='Completed')}/"
      f"{sum(1 for s in sprints if s['Status']=='In Progress')}/"
      f"{sum(1 for s in sprints if s['Status']=='Planned')})")
print(f"work items: {len(work_items)}")
print(f"builds: {len(builds)}")
print(f"support tickets: {len(tickets)}")
print(f"test runs: {len(test_runs)}")
