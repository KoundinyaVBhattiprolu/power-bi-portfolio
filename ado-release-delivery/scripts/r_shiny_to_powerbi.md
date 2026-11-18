# R Shiny → Power BI migration note

This is the story behind this project — and the strongest interview
story in Koundinya's portfolio. It is a migration note, not a
runnable script: **R was not run here (R is not installed on this
machine)**, so run the R code in RStudio if you want to verify it.
The Power BI side is fully built from the CSVs in `data/`.

## What existed first: R Shiny + Jenkins

The original reporting was an R Shiny web app, deployed with Jenkins
and a CI/CD pipeline, running against an on-premise server. Data was
wrangled in R (dplyr / janitor) from ADO exports, then served as an
interactive Shiny dashboard for the RTE, clients and stakeholders.

```r
# R Shiny (original, simplified) — the shape of the old app
library(shiny); library(dplyr); library(janitor)

work_items <- read.csv("ado_export.csv") %>%
  clean_names() %>%
  mutate(
    created_date = as.Date(created_date),
    closed_date  = as.Date(closed_date),
    is_bug   = work_item_type == "Bug",
    is_fixed = state %in% c("Closed", "Resolved")
  )

ui <- fluidPage(
  titlePanel("Release Delivery — ADO Reporting"),
  sidebarLayout(
    sidebarPanel(selectInput("release", "Release", choices = unique(work_items$release))),
    mainPanel(plotOutput("bug_burndown"), tableOutput("release_summary"))
  )
)

server <- function(input, output) {
  release_data <- reactive({ filter(work_items, release == input$release) })
  output$bug_burndown <- renderPlot({
    release_data() %>% filter(is_bug) %>%
      count(created_date, is_fixed) # created vs fixed over time
  })
}

shinyApp(ui, server)
```

Jenkins built and deployed the Shiny app on every push
(`Jenkinsfile`: install R packages → run tests → deploy to the
on-premise Shiny server). That worked — but every change meant
re-deploying a web app, and stakeholders had to go to a separate
portal instead of the reporting the rest of the org used.

## Why it moved: the team moved to Azure DevOps

When the team moved to Azure DevOps, the reporting moved with it:

| R Shiny era | Power BI era (this pack) |
|---|---|
| R wrangling (dplyr / janitor) on ADO exports | Python generator + Power Query, same cleaning rules |
| Shiny `reactive()` filters by release / sprint | Slicers on Release, Sprint, Team, Area |
| `count(created_date)` burndown in ggplot | DAX `Bugs Created in Period` vs `Bugs Fixed in Period` (USERELATIONSHIP on ClosedDate) |
| Jenkins deploys the Shiny app | ADO Pipelines builds in `builds_deployments.csv` — Jenkins 90.0% success vs ADO 92.4% in this sample |
| A separate portal stakeholders had to visit | One .pbix, published to a Power BI workspace, scheduled refresh |

## What stayed the same

The questions the reporting answers did not change — that is the
point to make in interviews:

1. **Are we delivering the next release?** → Release Readiness %
   (stories done / stories in scope).
2. **Are we winning against bugs?** → Bugs Created vs Bugs Fixed,
   Net Bug Change, Open Bugs by severity.
3. **Is quality leaking to customers?** → Defect Leakage %
   (bugs found in Production).
4. **Can RTE / clients / stakeholders see it?** → the same support
   and stakeholder views, now in Power BI instead of Shiny.

## The Python equivalent (actually run here)

The cleaning the R code did is now in `generate_ado_data.py`
(Python, seeded, reproducible). The messy-data → clean-data
pipeline from the main pack (`scripts/clean_sales_python.py`)
is the same pattern: wrangle first, model second, visualise last.
