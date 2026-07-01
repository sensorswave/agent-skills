---
name: wave-analytics
description: >-
  Analyze user behavior data with Sensors Wave MCP tools: event analysis,
  funnel analysis, retention analysis, user list queries, user event
  sequences, and custom SQL on Doris. Use when
  performing 数据分析, 用户行为分析, 漏斗分析, 留存分析, event metrics,
  conversion analysis, or ad-hoc SQL queries on Wave data. For saved charts
  or dashboards, hand off to wave-dashboard-builder.
---

# Wave Analytics

## Goal

Turn a user question into the right Wave analysis query, execute it with MCP tools, and explain the result as a business answer.

## Load When Needed

- Read [references/analysis-models.md](references/analysis-models.md) when constructing query parameters, filters, custom SQL, or a dashboard-builder handoff.

## Tools

- Metadata: `list_events`, `list_event_properties`, `list_user_properties`, `list_metrics`, `list_cohorts`
- Analysis: `query_event_analysis`, `query_funnel`, `query_retention`, `query_user_list`, `query_user_sequence`, `get_user_profile`, `query_cohort_user_count`
- SQL: `get_sql_schema`, `query_custom_sql`

## Workflow

1. Classify the request:
   - Metric/trend/breakdown -> event analysis
   - Step conversion/drop-off -> funnel
   - Return behavior after first action -> retention
   - Find users/cohort candidates -> user list or cohort count
   - Explain one user's behavior -> user sequence or user profile
   - Query not expressible by models -> custom SQL
   - Save or present reusable assets -> hand off to `wave-dashboard-builder`
2. Discover the data model before querying. Map business terms to actual event/property names.
3. Choose sane defaults only when the user did not specify them: recent 30 days, time unit by range, limit 10 for breakdowns, limit 100 for user lists, 7-day ordered funnel window.
4. Run the query tool. If it fails, fix concrete parameter issues first: event name, property name, operator, filter structure, or date range.
5. Explain the result with conclusion first, then supporting numbers, trend/comparison, caveats, and suggested next analysis.
6. If the user asks to save charts or build a dashboard, summarize the validated query shape and hand off to `wave-dashboard-builder`.

## Boundaries

- Do not design or implement new tracking here; hand off to `wave-tracking`.
- Do not run Tracking Plan QC here; hand off to `wave-tracking-qc`.
- Do not modify Catalog metadata here; hand off to `wave-catalog-governance`.
- Do not create saved charts or dashboards here; hand off to `wave-dashboard-builder`.
- For custom SQL, only use read-only SELECT queries and include a limit unless the user explicitly asks for an aggregate-only query.

## Output

Return:
- Short answer or verdict
- Key numbers in a compact table when useful
- Interpretation in business language
- Caveats about data scope, filters, or tracking quality
- One or two recommended follow-up queries

For dashboard requests, return the query shape and recommended chart type before handing off.
