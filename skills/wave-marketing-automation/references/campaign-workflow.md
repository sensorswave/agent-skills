# Campaign operation workflow

Use the smallest flow that matches the user's request. Read-only inspection,
planning, saving a Draft, testing, lifecycle operations, and performance review
have different side-effect boundaries.

## Planning and Draft creation

For a new Campaign or a copy/update that changes business behavior:

```text
get_ma_design_context
→ choose an existing connection
→ get_ma_connection_detail
→ get_ma_sms_assets (SMS only)
→ inspect/query the audience and validate any reusable cohort definition
→ plan_ma_campaign
→ validate_ma_campaign
→ save_ma_campaign
```

The plan passed to `validate_ma_campaign` and `save_ma_campaign` must be the
same complete plan. The brief is shown before the write; a model must not jump
from a numeric ID lookup directly to Campaign creation. Before
`save_ma_campaign`, ask the user to approve the complete validated Draft. A
request to design a Campaign alone does not authorize persistence.

`safe_to_save=false` blocks saving. `safe_to_launch=false` blocks launch or
resume. Resolve the concrete validation issue instead of explaining it away in
text.

## Config contracts

Write these fields instead of inferring them from an existing Campaign.

- `content_config` (Webhook): `{"body":"{\"ssid\":\"{{user.ssid}}\"}","variable_defaults":{"user.city":"unknown"}}`.
  Do not put the copy in `description`. WeCom/push JSON belongs in `body`.
- `content_config` (SMS): `{"sign_name":"...","template_id":"...","variable_bindings":{"name":{"mapping":"{{user.name}}","default":"用户"}}}`.
- `trigger_config`: `time_once` uses `fire_date`; `time_recurring` uses
  `granularity`/`n`/`start_date`/`fire_time`/`tz`; `action_done` uses
  `trigger_event` + `active_duration`; `action_done_not_done` also needs
  `delay` and `cancel_event`. Do not send `frequency` or `time`.
- `in_cohort`: `field.name=id`, `table_type=cohort`, `operator=in`,
  `values=[cohort_id]`.
- `test_ma_content` variables: only `user.*`, `event.*`, `campaign.id`,
  `campaign.name`. Never `message.*` or `content.*`.
- Empty `content_config` can `save` a Draft. `validate` reports
  `content_missing` as a launch blocker (`safe_to_launch=false`). Launch and
  test send require a real body.
- `context_id` is a snapshot hash. On `context_stale`, call
  `get_ma_design_context` and `plan_ma_campaign` again. Do not reuse the old
  plan.

When no suitable connection exists, pause Campaign planning at the Where
decision. If the user explicitly requests channel creation, run
`save_ma_connection → test_ma_connection → get_ma_connection_detail`, then get
a fresh MA design context before planning/validation so the new connection is
part of the evidence snapshot.

## Exact copy

For an exact copy explicitly requested by the user, `copy_ma_campaign` may be
used after reading the source Campaign detail. If the user wants any behavior,
audience, timing, content, channel, frequency, or goal changed, use the full
planning flow and validate the resulting plan.

## Read-only inspection

Use `list_ma_campaigns` before an unknown Campaign ID, then
`get_ma_campaign_detail`. Use `list_ma_connections` before an unknown
connection ID, then `get_ma_connection_detail`. Read-only inspection does not
require a complete 5W1H brief, but do not invent missing facts.

## Test and lifecycle

- `test_ma_content` invokes a real SMS/Webhook delivery path. Explain the
  destination/side effect and require the user's explicit test request before
  calling it.
- `transition_ma_campaign` can launch, resume, pause, or stop a Campaign. Launch
  and resume can cause real customer delivery; require explicit user intent and
  the server confirmation flow.
- If the user did not request launch/resume, leave a successful save in Draft.
- Use `list_ma_campaign_operation_logs` to explain state changes or automatic
  pauses.

## Connection lifecycle

- Create/update: read existing candidates first. Call `save_ma_connection` only
  for an explicit channel-management request. Update uses the current
  `expected_version`; omitted fields remain unchanged.
- Test: call `test_ma_connection` only after explaining the real destination
  and side effect. A passing result updates the connection test status.
- Delete: read the current safe detail, show ID/name/references, then call
  `delete_ma_connection` only after explicit deletion confirmation. Never infer
  deletion permission from a request to design or clean up a Campaign.

## Performance review

1. Read `get_ma_campaign_dashboard` to obtain the attribution window and query
   template.
2. Use the returned query shape with `query_event_analysis` or `query_funnel`
   when deeper conversion analysis is needed.
3. Combine sent, delivered, failed, goal conversion, frequency governance,
   operation logs, and tracking caveats. Distinguish delivery from conversion.

For broad trend, funnel, retention, user behavior, or SQL interpretation,
hand off to `wave-analytics` after preserving the Campaign context.

## Stop conditions

Stop for clarification when a material 5W1H section is unresolved, no matching
tested connection exists, a required SMS asset cannot be bound, validation is
unsafe, or the user has not authorized a side-effecting operation.
