# Marketing brief format

Use this reference for Campaign design, creation, copy-with-changes, and
updates. The brief is a decision record, not a decorative summary. It must be
grounded in `get_ma_design_context` and other project-scoped tool results.

## Required shape

Present the brief as a fenced `wave-ma-brief` block. The JSON object contains:

```json
{
  "why": {
    "summary": "业务目标和成功指标",
    "evidence_status": "user_confirmed",
    "evidence": [],
    "open_questions": []
  },
  "who": {
    "summary": "目标受众、排除条件和样本验证",
    "evidence_status": "tool_inferred",
    "evidence": [],
    "open_questions": []
  },
  "when": {
    "summary": "触发条件、延迟、活动时段和时区",
    "evidence_status": "needs_confirmation",
    "evidence": [],
    "open_questions": ["..."]
  },
  "where": {
    "summary": "通道和已选连接",
    "evidence_status": "tool_inferred",
    "evidence": [],
    "open_questions": []
  },
  "what": {
    "summary": "Webhook body 或 SMS 资产和变量绑定",
    "evidence_status": "tool_inferred",
    "evidence": [],
    "open_questions": []
  },
  "how": {
    "summary": "频控、静默、重入、失败策略和效果衡量",
    "evidence_status": "user_confirmed",
    "evidence": [],
    "open_questions": []
  },
  "channel_strategy": {
    "mode": "reuse_existing",
    "connection_id": 32,
    "connection_name": "订单通知",
    "channel": "webhook",
    "provider": "",
    "test_status": "passed",
    "connection_version": 3,
    "reason": "项目中存在满足渠道和 provider 要求的已测试通道"
  },
  "assumptions": []
}
```

The actual IDs, names, status, and versions must come from tool results. The
example values are illustrative only and must never be copied into a real
Campaign.

## Evidence status

- `user_confirmed`: explicitly stated or approved by the user;
- `tool_inferred`: directly supported by a current project tool result;
- `needs_confirmation`: missing or ambiguous and material to execution.

Every section needs one status. Add short evidence references or facts when
they materially support the decision. Do not silently turn an assumption into
a confirmed fact.

## Mapping to Campaign configuration

- Why → `goal_config` and the conversion event/metric definition;
- Who → `audience_config`, exclusion conditions, cohort references, and sample
  or estimate checks;
- When → `trigger_config`, delay, schedule, timezone, and active window;
- Where → `channel`, `connection_id`, and `channel_strategy`;
- What → `content_config`: Webhook `{body, variable_defaults}` or SMS
  `{sign_name, template_id, variable_bindings}` from the selected connection
  and approved SMS assets. Do not leave the copy in `description`.
- How → frequency flags, silence/discard/defer policy, re-entry, and reporting
  interpretation.

Before `save_ma_campaign`, all material `needs_confirmation` items must be
resolved. Non-material assumptions can remain in `assumptions` and must be
shown in the confirmation summary.

## Minimal clarification rule

Ask one question per turn: the unresolved decision with the largest impact on
audience, trigger timing, connection, content, frequency, or goal definition.
Do not ask a long questionnaire when a tool can resolve the fact.
