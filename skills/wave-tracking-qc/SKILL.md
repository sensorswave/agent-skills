---
name: wave-tracking-qc
description: >-
  Run Sensors Wave tracking quality checks after events are already firing. Use
  when validating a published Tracking Plan against actual data, checking
  missing events or properties, or handling rollout acceptance. For Tracking
  Plan write/publish, SDK integration, or code fixes, route to wave-tracking.
---

# Wave Tracking QC

## Goal

Validate actual event data against a published Tracking Plan and return an acceptance result with concrete fix targets.

## Load First

- Read [policies/operating-rules.md](policies/operating-rules.md) before project-level MCP calls.
- Read [prompts/interaction.md](prompts/interaction.md) when confirmation wording is needed.
- Read [playbooks/tracking-qc.md](playbooks/tracking-qc.md) before calling the quality-check tool.

## Tools

- Project and baseline: `list_projects`, `list_tracking_plans`, `get_tracking_plan_detail`
- Quality check: `get_tracking_plan_quality_check`
- Cross-checks: `list_events`, `list_event_properties`, `list_pipelines`

## Preconditions

- The user must have a project and a Tracking Plan baseline.
- The plan should be published before QC. If it is not published, hand off to `wave-tracking`.
- The user must confirm the app/service has been rebuilt/redeployed/restarted if code changed.
- The user must confirm key events are already firing.
- The user must explicitly ask to begin QC. "事件触发了" alone is not enough.

## Workflow

1. Confirm project and plan. If the user does not provide a plan id, list plans and ask them to choose.
2. Confirm the plan status and explain limitations if it is not published.
3. Confirm runtime verification and explicit consent to start QC.
4. Call `get_tracking_plan_quality_check`.
5. Summarize the result as pass/fail plus issue list. Group issues by event, property, platform/pipeline if available, and likely fix owner.
6. Use cross-check tools only when the QC result is ambiguous or the user asks for deeper diagnosis.

## Boundaries

- Do not modify Tracking Plans, SDK code, Pipeline settings, or Catalog metadata from this skill.
- Do not infer that missing data is fixed until a later QC run confirms it.
- Do not run analytics interpretation here; hand off to `wave-analytics` for trend, funnel, retention, or SQL investigation.

## Output

Return:
- Acceptance verdict: passed, failed, or blocked by missing prerequisite.
- Evidence: plan id/name/status and checked scope.
- Issues: missing events, missing properties, no recent data, unexpected value coverage, or partial implementation.
- Next action: route each issue to `wave-tracking`, `wave-catalog-governance`, or `wave-analytics`.

## Stop

Stop after reporting the QC result. Wait for the user to decide whether to fix tracking, update Catalog metadata, or run analysis.
