---
name: wave-dashboard-builder
description: >-
  Build and maintain Sensors Wave saved charts and dashboards. Use when the
  user asks to create, update, organize, or polish charts, KPI cards,
  dashboards, overview pages, dashboard layouts, or reusable analysis assets.
  Use Wave MCP chart and dashboard tools; for exploratory data interpretation,
  route to wave-analytics first. For custom SQL, route to wave-sql-query.
---

# Wave Dashboard Builder

## Goal

Create or update saved Wave analysis assets: charts, dashboards, and dashboard layouts.

## Tools

- Project: `list_projects`
- Discover assets: `list_charts`, `list_dashboards`, `get_chart_detail`, `get_dashboard_detail`
- Create dashboards: `create_dashboard`
- Create charts: `create_event_chart`, `create_event_charts`, `create_funnel_chart`, `create_retention_chart`, `create_custom_sql_chart`
- Validate query shapes when needed: `query_event_analysis`, `query_funnel`, `query_retention`, `get_sql_schema`, `query_custom_sql`
- Polish layout: `set_dashboard_chart_layouts`
- Update existing assets: `update_dashboard`, `update_chart`

## Project gate

Before any other project-level MCP call:

1. Call `list_projects` and show a table of `project_id | name`.
2. Wait for the user to reply with a numeric `project_id`.
3. Only skip a new selection if the user already fixed this conversation to one project, or explicitly says to keep the current project without switching.

Never silently pick a project, and never list, create, update, or layout charts/dashboards before this step.

## Workflow

1. Pass the project gate first. Then clarify the asset target: standalone chart, new dashboard, existing dashboard, or dashboard refresh.
2. Discover existing dashboards/charts before creating duplicates when the user names an asset or asks to update. If the user asks what dashboards/charts exist, call `list_dashboards` / `list_charts` with no `search_key` and show every item (`total` plus pages). Do not search with type words like 看板, dashboard, 概览, or 图表.
3. Confirm the metric/query shape. If the user has not specified metrics clearly, hand off to `wave-analytics` or `wave-sql-query`, or run a lightweight validation query before creating assets.
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
7. After charts exist on a dashboard, call `get_dashboard_detail` before any layout change. `list_dashboards` / `get_resource(dashboard)` / `list_charts` do not include coordinates.

## Layout Defaults

Follow the Wave overview editor Speedy Layout. Every chart type uses the same height, including Metric/KPI cards.

- 12-column grid. Always `h=7`. `min_w=3`, `min_h=4`.
- Speedy layout is the default polish (单列 / 双列 / 三列 / 整理布局). Prefer `set_dashboard_chart_layouts` with `speedy_columns` so the server sorts by visual order (`y` then `x`) and applies:
  - 1 column: `w=12 h=7`
  - 2 columns: `w=6 h=7`
  - 3 columns: `w=4 h=7`
- Do not give Metric/KPI a shorter height or a special top row. Treat them like any other chart.
- New chart without layout: `w=12 h=7` at the bottom (`x=0`, `y=max(y+h)`).
- Copy keeps the source `w/h` and appends at the bottom.
- Custom `layouts` may change `x/w` if the user asks, but keep `h=7` unless they explicitly request another height.
- `x+w` must fit the 12-column grid. Rectangles must not overlap each other or charts not listed in the call. On overlap, include every affected chart or use `speedy_columns`.

## Boundaries

- Do not discover or write project assets before the user selects a `project_id`.
- Do not invent analysis meaning when the metric definition is unclear; validate with `wave-analytics` or `wave-sql-query`.
- Do not run Tracking Plan validation here; hand off to `wave-tracking-validation`.
- Do not design new tracking events here; hand off to `wave-tracking`.
- Do not delete charts or dashboards unless the user explicitly asks and confirms the exact asset name. Prefer create/update/layout operations.

## Output

Return:
- Created or updated dashboard ids/names
- Created or updated chart ids/names/types
- Layout changes applied (`speedy_columns` or per-chart `x,y,w,h`)
- Any chart requests skipped and why
- Suggested follow-up if data validation or metric definition is still unclear
