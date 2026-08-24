---
name: wave-tracking-validation
description: >-
  Validate Sensors Wave tracking after events are already firing. Use when
  comparing a published Tracking Plan against actual data, checking
  missing events or properties, or handling rollout acceptance. For Tracking
  Plan write/publish, SDK integration, or code fixes, route to wave-tracking.
---

# Wave Tracking Validation

## Goal

Validate actual event data against a published Tracking Plan and return an acceptance result with concrete fix targets.

## Load First

- Read [policies/operating-rules.md](policies/operating-rules.md) before project-level MCP calls.
- Read [prompts/interaction.md](prompts/interaction.md) when confirmation wording is needed.
- Read [playbooks/tracking-validation.md](playbooks/tracking-validation.md) before calling the quality-check tool.

## Tools

- Project and baseline: `list_projects`, `list_tracking_plans`, `get_tracking_plan_detail`
- Quality check: `get_tracking_plan_quality_check`
- Cross-checks: `list_events`, `list_event_properties`, `list_pipelines`

## Preconditions

- The user must have a project and a Tracking Plan baseline.
- The plan should be published before validation. If it is not published, hand off to `wave-tracking`.
- The user must confirm the app/service has been rebuilt/redeployed/restarted if code changed.
- The user must confirm key events are already firing.
- The user must explicitly ask to begin validation. "事件触发了" alone is not enough.

## Workflow

1. Pass the project gate first: `list_projects`, show `project_id | name`, and wait for a numeric `project_id` unless the user already fixed this conversation to one project or explicitly says to keep the current project without switching. Then confirm the plan. If the user does not provide a plan id, list plans and ask them to choose.
2. Confirm the plan status and explain limitations if it is not published.
3. Confirm runtime verification and explicit consent to start validation.
4. Call `get_tracking_plan_quality_check`.
5. Summarize the result as pass/fail plus issue list. Group issues by event, property, platform/pipeline if available, and likely fix owner.
6. Use cross-check tools only when the validation result is ambiguous or the user asks for deeper diagnosis.

## Boundaries

- Do not call quality-check or other project-level tools before the user selects a `project_id`.
- Do not modify Tracking Plans, SDK code, Pipeline settings, or Catalog metadata from this skill.
- Do not infer that missing data is fixed until a later validation run confirms it.
- Do not run analytics interpretation here; hand off to `wave-analytics` for trend, funnel, retention, or SQL investigation.

## Output

Return:
- Acceptance verdict: passed, failed, or blocked by missing prerequisite.
- Evidence: plan id/name/status and checked scope.
- Issues: missing events, missing properties, no recent data, unexpected value coverage, or partial implementation.
- Next action: route each issue to `wave-tracking`, `wave-catalog-governance`, or `wave-analytics`.

## Stop

Stop after reporting the validation result. Wait for the user to decide whether to fix tracking, update Catalog metadata, or run analysis.
