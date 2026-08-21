---
name: wave-dashboard-builder
description: >-
  Build and maintain Sensors Wave saved charts and dashboards. Use when the
  user asks to create, update, organize, or polish charts, KPI cards,
  dashboards, overview pages, dashboard layouts, or reusable analysis assets.
  Use Wave MCP chart and dashboard tools; for exploratory data interpretation,
  route to wave-analytics first.
---

# Wave Dashboard Builder

## Goal

Create or update saved Wave analysis assets: charts, dashboards, and dashboard layouts.

## Tools

- Project: `list_projects`
- Discover assets: `list_charts`, `list_dashboards`, `get_chart_detail`
- Create dashboards: `create_dashboard`
- Create charts: `create_event_chart`, `create_event_charts`, `create_funnel_chart`, `create_retention_chart`, `create_custom_sql_chart`
- Validate query shapes when needed: `query_event_analysis`, `query_funnel`, `query_retention`, `get_sql_schema`, `query_custom_sql`
- Polish layout: `set_dashboard_chart_layouts`
- Update existing assets: `update_dashboard`, `update_chart`

## Workflow

1. Clarify the asset target: standalone chart, new dashboard, existing dashboard, or dashboard refresh.
2. Discover existing dashboards/charts before creating duplicates when the user names an asset or asks to update.
3. Confirm the metric/query shape. If the user has not specified metrics clearly, hand off to `wave-analytics` or run a lightweight validation query before creating assets.
4. Choose chart types deliberately:
   - KPI totals -> `Metric`
   - Time trends -> `Line`
   - Category comparison -> `Column` or `Bar`
   - Composition -> `StackedLine`, `StackedColumn`, or `Pie`
   - Funnel conversion -> `FunnelColumn`
   - Retention curve -> `Line`
   - SQL/detail table -> `Table`
5. For a dashboard, prefer one batch call when creating multiple event charts with `create_event_charts`.
6. Use `new_dashboards` when creating a dashboard together with charts; use `dashboard_ids` when attaching to an existing dashboard.
7. Apply layout only after chart creation if default auto-layout is not enough.

## Layout Defaults

- KPI row: `w=3 h=3`, four cards across.
- Standard trend/comparison charts: `w=6 h=5`, two-column grid.
- High-priority trend, table, funnel graph: `w=12 h=6`.
- Pie or compact composition chart: `w=4 h=5` or `w=6 h=5`.
- Put KPI cards at `y=0`; put diagnostic/detail charts below.
- Layouts are validated server-side: `x+w` must fit the 12-column grid, and rectangles must not overlap each other or charts not listed in the call. On an overlap error, resend one call covering every affected chart.

## Boundaries

- Do not invent analysis meaning when the metric definition is unclear; validate with `wave-analytics`.
- Do not run Tracking Plan validation here; hand off to `wave-tracking-validation`.
- Do not design new tracking events here; hand off to `wave-tracking`.
- Do not delete charts or dashboards unless the user explicitly asks and confirms the exact asset name. Prefer create/update/layout operations.

## Output

Return:
- Created or updated dashboard ids/names
- Created or updated chart ids/names/types
- Layout changes applied
- Any chart requests skipped and why
- Suggested follow-up if data validation or metric definition is still unclear
