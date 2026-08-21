---
name: wave-marketing-automation
description: >-
  Plan and operate Sensors Wave marketing automation with real project assets.
  Use for 5W1H Campaign briefs, reusable SMS/Webhook channel selection,
  audience planning, Campaign validation, Draft creation, testing, lifecycle
  operations, and Campaign performance review. For generic data analysis use
  wave-analytics; for product usage questions use wave-product-help.
---

# Wave Marketing Automation

## Goal

Turn a marketing request into an evidence-backed, executable Wave Campaign plan
and carry out only the lifecycle operation the user requested. Use the current
project's events, properties, metrics, cohorts, Campaigns, governance rules,
and existing connections as the source of truth. Do not replace MA operations
with generic marketing advice or invented configuration.

## Load When Needed

- Read [references/campaign-workflow.md](references/campaign-workflow.md) for
  operation-specific tool sequences, confirmation boundaries, and review flow.
- Read [references/5w1h-brief.md](references/5w1h-brief.md) before designing,
  creating, copying with changes, or updating a Campaign.
- Read [references/channel-reuse.md](references/channel-reuse.md) before
  selecting a channel, configuring content, testing, or saving a Campaign.

## Tools

- Project and context: `list_projects`, `get_ma_design_context`
- Existing assets: `list_cohorts`, `get_cohort_detail`, `list_ma_connections`,
  `get_ma_connection_detail`, `get_ma_sms_assets`, `list_ma_campaigns`,
  `get_ma_campaign_detail`, `get_ma_governance`
- Channel management: `save_ma_connection`, `test_ma_connection`,
  `delete_ma_connection`
- Audience checks: `validate_cohort_definition`, `query_cohort_user_count`,
  `sample_cohort_users`, `inspect_ma_audience`, `create_cohort`,
  `update_cohort`, `recalculate_cohort`, `get_cohort_run_status`
- Campaign planning: `plan_ma_campaign`, `validate_ma_campaign`,
  `save_ma_campaign`, `copy_ma_campaign`
- Lifecycle and content: `test_ma_content`, `transition_ma_campaign`,
  `list_ma_campaign_operation_logs`
- Review: `get_ma_campaign_dashboard`, `query_event_analysis`, `query_funnel`

## Workflow

1. Classify the request as one of the following:
   - design/create/copy-with-changes/update: use the 5W1H planning flow;
   - read/list/detail/status: inspect the requested asset without forcing a
     new brief;
   - test/launch/resume/pause: inspect the current Campaign and connection,
     explain the side effect, then use the lifecycle flow;
   - performance review: use the Campaign dashboard and, when needed, hand
     the validated metric shape to `wave-analytics`.
2. Confirm the project before project-level MCP calls unless the user has
   explicitly fixed the current project. Never silently choose a project.
3. For Campaign design, call `get_ma_design_context` first. Discover real
   events, properties, metrics, cohorts, Campaigns, existing connections,
   governance, and the returned `context_id` before proposing configuration.
4. Produce a structured `wave-ma-brief` with all six sections: Why, Who,
   When, Where, What, and How. Keep evidence status visible and ask one
   focused clarification question when a key decision still changes audience,
   timing, channel, content, frequency, or success measurement.
5. Prefer a matching existing connection. Select by `connection_id`, read its
   safe detail, and use the real channel/provider/test status. If no suitable
   connection exists, record `channel_strategy.mode=new`. Create one with
   `save_ma_connection` only when the user explicitly requests it, has supplied
   the complete channel configuration and write-only credentials, and accepts
   the confirmation boundary. Test the saved connection with
   `test_ma_connection`, then read its detail again before resuming Campaign
   planning. Do not create a duplicate merely because a candidate is untested.
6. Build the Campaign plan with `plan_ma_campaign`, then validate the complete
   plan with `validate_ma_campaign`. Write webhook `body` or SMS
   `sign_name`/`template_id`/`variable_bindings` into `content_config`; do not
   leave the copy in `description`. If `context_id` is stale, refresh
   `get_ma_design_context` and re-plan. Do not rebuild or silently alter the
   plan after validation. If `safe_to_save` is false, clarify or repair the
   plan before saving. Empty content can save a Draft but cannot launch.
7. Before calling `save_ma_campaign`, present the complete 5W1H brief and the
   validated plan and ask for explicit confirmation to persist the Draft. Save
   only the exact validated plan. If the host or server supplies a separate
   confirmation flow, honor it. A user request to design a Campaign is not
   permission to persist it, send messages, or launch it.
8. Call `test_ma_content`, `transition_ma_campaign` for launch/resume/pause, or
   other side-effecting operations only when the user explicitly requests that
   operation and the immediate confirmation boundary has been satisfied. If a
   user did not ask to launch, leave the result as a Draft.
9. Update or delete a connection only when the user explicitly requests that
   connection-management operation. Read the current detail first; updates use
   `connection_id` plus `expected_version`, and deletion uses `connection_id`
   plus the exact current `expected_name`. Never delete a connection as a
   Campaign-planning cleanup step.
10. For review, establish the attribution window and Campaign state first, then
   combine dashboard results, operation logs, delivery status, frequency
   governance, and goal conversion. State data scope and unresolved tracking
   caveats.

## Non-negotiable boundaries

- Never invent event names, properties, metric definitions, cohort IDs,
  Campaign IDs, connection IDs, SMS signs/templates, Webhook bodies, or
  provider details.
- `connection_id` and `Connection` remain the MA code/API contract. User-facing
  language should say “通道”, but do not rename or reinterpret the contract.
- `channel` is a channel type; a selected connection is an existing project
  entity. Do not create a new connection merely because the requested type is
  SMS or Webhook.
- Never put Webhook URL/method/header/secret or SMS provider credentials into
  Campaign `content_config`. Use the selected connection and approved SMS
  assets.
- Connection credentials are write-only inputs to `save_ma_connection`. Never
  repeat them in summaries, tool output, examples, or follow-up messages.
- Keep `use_project_frequency` explicit. If enabled, read governance and
  explain the applicable project/channel rules in How.
- A cohort is reusable audience state; an inline audience is acceptable for a
  simple one-off filter. Do not create a cohort only to implement a real-time
  trigger.
- Do not call launch/resume or send/test tools because the plan appears valid.
  Validity is not user authorization.
- `test_ma_connection` tests the saved connection itself and updates its latest
  test status. `test_ma_content` tests Campaign content and variable bindings;
  it does not establish that the connection is launch-ready.

## Handoffs

- For metric, funnel, retention, user behavior, or SQL interpretation after
  the Campaign context is established, hand off to `wave-analytics`.
- For saved charts or dashboards, hand off to `wave-dashboard-builder` with the
  validated metric/query shape.
- For tracking implementation or tracking validation, use the corresponding
  tracking skills instead of treating missing events as a Campaign problem.
- For Wave navigation, permissions, or feature explanations, use
  `wave-product-help`.

## Output

- Planning: concise 5W1H brief, evidence status, selected/rejected channel
  candidates, assumptions, open questions, and the next gated operation.
- Save: Campaign name/id/status, validation result, confirmation state, and
  whether anything was actually sent or launched.
- Lifecycle: operation, Campaign state before/after, side-effect summary, and
  server result.
- Review: goal and audience, trigger, channel/content, frequency/silence,
  sent/delivered/failed/converted numbers, attribution window, and caveats.

## Stop

Stop and ask the user when a key 5W1H decision is unresolved, no suitable
tested connection exists and the user has not authorized creating/testing one,
validation is unsafe, the requested operation would save credentials, call an
external channel, delete, send, or launch without explicit authorization, or
the required MCP tool is not available.
