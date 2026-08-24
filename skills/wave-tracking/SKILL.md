---
name: wave-tracking
description: >-
  Plan and implement Sensors Wave tracking from code, PRDs, or user flows.
  Use when designing events and properties, deciding client/server ownership,
  defining identify/reset strategy, writing or publishing Tracking Plans,
  creating/using Pipelines, or generating SDK integration guidance. For
  live tracking validation, route to wave-tracking-validation. For saved charts or dashboards,
  route to wave-dashboard-builder.
---

# Wave Tracking

## Goal

Produce or execute a tracking rollout that a product/engineering team can use, with the Tracking Plan as the mainline and a published plan as the required baseline before Pipeline/SDK integration, code changes, or dashboard handoff.

## Load First

- Read [policies/operating-rules.md](policies/operating-rules.md) before any project-level MCP call or write operation.
- Read [prompts/interaction.md](prompts/interaction.md) when you need the exact confirmation wording.

## Load When Needed

- Code or PRD discovery: [playbooks/code-discovery.md](playbooks/code-discovery.md)
- Draft output format: [playbooks/draft-output.md](playbooks/draft-output.md)
- Event/property design rules: [references/tracking-principles.md](references/tracking-principles.md)
- Login, logout, anonymous-to-login, cross-device: [references/user-identification.md](references/user-identification.md)
- Pipeline/SDK setup and documentation links: [references/sdk-matrix.md](references/sdk-matrix.md)
- Tracking Plan write/publish: [playbooks/tracking-plan.md](playbooks/tracking-plan.md)

## Tools

- Project and discovery: `list_projects`, `list_events`, `list_event_properties`, `list_user_properties`
- Tracking Plan: `list_tracking_plans`, `get_tracking_plan_detail`, `list_templates`, `get_template_detail`, `save_tracking_plan`, `publish_tracking_plan`
- Pipeline/SDK: `list_pipelines`, `get_pipeline_detail`, `create_pipeline`

## Workflow

1. Classify the request as design-only or rollout. Treat Pipeline/SDK integration, code changes, and dashboard handoff as rollout stages downstream of the Tracking Plan.
2. Pass the project gate before any other project-level MCP call: `list_projects`, show `project_id | name`, and wait for a numeric `project_id`. Only skip a new selection if the user already fixed this conversation to one project, or explicitly says to keep the current project without switching. Never silently choose a project.
3. Discover existing Catalog and Tracking Plans before inventing names or creating a new plan.
4. For design work, produce a draft with events, trigger timing, platform/client/server ownership, properties, required flags, and identify/reset handling.
5. For Tracking Plan writes, present the complete draft snapshot before calling `save_tracking_plan`; include a warning that omitted events/properties may be removed when replacing an existing draft.
6. Use a published Tracking Plan as a hard gate for every downstream rollout stage. If an existing published plan is selected unchanged, read its detail and use it as the baseline. If the selected plan is a draft, or this flow creates or updates a plan, save the complete draft, immediately request explicit publish confirmation, and publish it in this flow before proceeding.
7. Never call Pipeline tools, provide project-specific SDK integration or tracking code, edit tracking code, or hand off to dashboard building while the baseline plan is unpublished. If the user declines or postpones publication, stop at the draft and explain that downstream work is blocked by the unpublished plan.
8. Publish only after explicit user confirmation. Do not infer confirmation from a request to continue with implementation.
9. For SDK/Pipeline work after publication, use MCP-returned `endpoint` and `source_token`; do not construct them manually.
10. If the user asks for charts or a dashboard after publication, hand off to `wave-dashboard-builder` with the relevant events, properties, and intended metrics.

## Boundaries

- Do not call Catalog, Tracking Plan, Pipeline, or SDK tools before the user selects a `project_id`.
- Do not run live tracking validation from this skill. Hand off to `wave-tracking-validation` only after the user confirms events are firing and asks to check.
- Do not maintain existing Catalog documentation fields here. Hand off to `wave-catalog-governance`.
- Do not perform deep data interpretation here. Hand off to `wave-analytics`.
- Do not create saved charts or dashboards here. Hand off to `wave-dashboard-builder`.
- Do not restart, redeploy, rebuild, or operate the user's app/device/server. Tell the user what they must run manually.

## Output

- Design draft: event table, property table, identify/reset plan, open questions.
- Write/publish result: plan id/name/status and what changed.
- SDK result: chosen pipeline, endpoint/source_token source, SDK doc link, initialization and identify/reset placement.
- Dashboard request handoff: summarize target events, metrics, and suggested chart types for `wave-dashboard-builder`.

## Stop

Stop at an unpublished draft unless the user explicitly confirms publication and publication succeeds. After code/SDK changes, ask the user to manually restart/redeploy and verify events are firing before any validation handoff.
