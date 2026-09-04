# Channel reuse and content rules

## Selection order

1. Read `get_ma_design_context` and inspect its `connections` capability.
2. If needed, call `list_ma_connections` with the requested channel/provider
   filters.
3. Choose one existing project connection by its `connection_id`.
4. Call `get_ma_connection_detail` before planning the Campaign content.
5. For SMS, call `get_ma_sms_assets` and select an approved sign/template whose
   variables can be completely bound.

The UI calls these resources “通道”. The MA API and code continue to use
`Connection`, `connection_id`, and `ConnectionService`. Preserve those names in
tool input and output even when explaining them to a user.

## Matching criteria

Prefer a connection that matches:

- required channel (`sms` or `webhook`);
- required provider for SMS;
- latest test status (`passed` is required before launch);
- compatible rate limit and project frequency governance;
- required template variables or payload shape;
- existing Campaign references only as a planning signal, not as a reason to
  expose secrets.

If several candidates match, explain the choice briefly using tool evidence.
Do not select by name alone when provider, test status, or version changes the
execution result.

## New connection path

`channel_strategy.mode = "new"` can record that no existing connection matches,
but it does not authorize creation. If the user explicitly asks to create the
channel and supplies the complete configuration and credentials, call
`create_ma_connection` after the confirmation boundary, then call
`test_ma_connection` after a separate explicit test request. Read the new
connection detail again and use its real `connection_id`, version, and test
status before returning to Campaign planning.

Do not invent a `connection_id`, inline a Webhook URL into Campaign content, or
embed SMS provider credentials in Campaign configuration. Do not create a new
connection merely because a matching existing connection is untested; offer to
test the existing entity first.

## Connection management

- `create_ma_connection` creates a new connection. `update_ma_connection`
  requires `connection_id + expected_version`. Read detail before update.
- Treat every credential as write-only. Never echo it after the tool call.
- `test_ma_connection` tests the saved URL/auth/provider configuration and
  updates `test_status`; it performs a real external request or SMS send.
- `test_ma_content` tests Campaign content/variable bindings and does not update
  the connection's launch gate status.
- `delete_ma_connection` requires the current `connection_id` and exact
  `expected_name`. Call it only for an explicit deletion request. Existing
  Campaign references block deletion; never delete a connection to make a new
  Campaign plan simpler.

## Content boundaries

- Webhook Campaigns store only the body/defaults needed by the selected
  connection. URL, method, headers, authentication, and secrets stay in the
  connection.
- SMS Campaigns store the approved sign, template, and complete variable
  bindings. Provider credentials, callback URLs, and callback tokens stay out
  of the Campaign.
- If the required template variable cannot be sourced from real project
  attributes or a supported binding, mark What as `needs_confirmation` and
  stop before validation or create/update.

## Launch gate

Never launch or resume a Campaign when its selected connection's latest test
is not passed. SMS assets are rechecked by the server at launch time. A valid
connection is not permission to send: launch and test still require the user's
explicit operation request and the server confirmation flow.
