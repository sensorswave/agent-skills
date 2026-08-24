---
name: wave
description: >-
  Sensors Wave platform router skill. Use when the user asks a broad or
  ambiguous Wave question and you need to route to tracking implementation
  (wave-tracking), tracking validation (wave-tracking-validation), analytics
  (wave-analytics), marketing automation (wave-marketing-automation),
  dashboard building (wave-dashboard-builder), product help
  (wave-product-help), or Catalog governance (wave-catalog-governance).
---

# Wave

## Goal

Route the user to exactly one concrete Wave skill, then read that skill and follow it. Do not execute domain work from this router.

## Routing

- Tracking implementation -> read [../wave-tracking/SKILL.md](../wave-tracking/SKILL.md)
  Use for event design, code/PRD discovery, client/server ownership, identify/reset strategy, Tracking Plan draft/write/publish, Pipeline selection/creation, SDK integration, and preparing tracking context for dashboard handoff. Treat the published Tracking Plan as the required baseline before implementation or other downstream stages.
- Tracking validation -> read [../wave-tracking-validation/SKILL.md](../wave-tracking-validation/SKILL.md)
  Use only after events are firing and the user wants Tracking Plan validation, rollout acceptance, or missing event/property checks.
- Analytics -> read [../wave-analytics/SKILL.md](../wave-analytics/SKILL.md)
  Use for event metrics, funnel, retention, user list, user sequence, user profile, and custom SQL.
- Marketing automation -> read
  [../wave-marketing-automation/SKILL.md](../wave-marketing-automation/SKILL.md)
  Use for 5W1H Campaign design, reusable SMS/Webhook connection selection,
  audience planning, Campaign validation, Draft creation, testing, lifecycle
  operations, and Campaign performance review.
- Dashboard building -> read [../wave-dashboard-builder/SKILL.md](../wave-dashboard-builder/SKILL.md)
  Use when the user asks to create, update, organize, or polish saved charts, dashboards, overview pages, KPI cards, dashboard layouts, or reusable analysis assets.
- Product help -> read [../wave-product-help/SKILL.md](../wave-product-help/SKILL.md)
  Use for product usage, setup steps, concepts, FAQ, page entry, permission, and troubleshooting questions.
- Catalog governance -> read [../wave-catalog-governance/SKILL.md](../wave-catalog-governance/SKILL.md)
  Use for maintaining existing Catalog display names, descriptions, event trigger conditions, platform tags, and example values.

## Disambiguation

- If the request mixes tracking and analytics, finish the tracking design or implementation path first, then hand off to analytics.
- If the request mixes tracking implementation and validation, do implementation in `wave-tracking`; only run validation after the user confirms events are already firing and explicitly asks to check.
- If the request asks to analyze data and then save the result as charts or dashboards, run analytics first for the metric/query shape, then hand off to `wave-dashboard-builder`.
- If the request mixes Campaign planning and performance analysis, complete the
  Campaign context and operation gate in wave-marketing-automation first, then
  hand off the validated metric shape to wave-analytics.
- If the request mixes Campaign planning and saved dashboard creation, complete
  the Campaign context first, then hand off the metric/query shape to
  wave-dashboard-builder.
- If the request asks to change technical names, data types, delete metadata, or merge duplicates, route to `wave-catalog-governance` only to explain the current MCP boundary; do not imply those operations are currently available.
- If the user asks "Wave 怎么用 / 在哪配置 / 为什么看不到", prefer `wave-product-help` over analytics or tracking.

## Stop

After choosing a route, stop using this file and follow the target skill. Project-scoped skills (`wave-tracking`, `wave-tracking-validation`, `wave-analytics`, `wave-marketing-automation`, `wave-dashboard-builder`, `wave-catalog-governance`) must confirm `project_id` via `list_projects` before any other project-level MCP call. If no route is clear, ask one concise question: "你现在要做埋点落地、质检、数据分析、营销自动化、看板构建、产品帮助，还是 Catalog 元数据治理？"
