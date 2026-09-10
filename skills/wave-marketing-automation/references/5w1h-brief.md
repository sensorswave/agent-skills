# 营销简报格式

用于 Campaign 的设计、创建、带改动复制和更新。简报是决策记录，不是装饰性摘要，必须建立在 `get_ma_design_context` 和其他项目级工具结果之上。

## 必需形态

用围栏代码块 `wave-ma-brief` 展示简报。JSON 对象包含：

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

真实的 ID、名称、状态和版本必须来自工具结果。示例值仅作说明，绝不能照搬进真实 Campaign。

## 证据状态

- `user_confirmed`：用户明确说明或认可；
- `tool_inferred`：有当前项目的工具结果直接支撑；
- `needs_confirmation`：缺失或含糊，且对执行有实质影响。

每个部分都要有一个状态。当证据对决策有实质支撑时，附上简短的证据引用或事实。不要把假设悄悄变成已确认的事实。

## 到 Campaign 配置的映射

- Why → `goal_config` 以及转化事件/指标定义；
- Who → `audience_config`、排除条件、分群引用，以及抽样或估算检查；
- When → `trigger_config`、延迟、排期、时区和活动窗口；
- Where → `channel`、`connection_id` 和 `channel_strategy`；
- What → `content_config`：来自所选通道和已审核 SMS 资产的 Webhook `{body, variable_defaults}` 或 SMS `{sign_name, template_id, variable_bindings}`。不要把文案留在 `description`。
- How → 频控开关、静默/丢弃/延后策略、重入，以及报表解读。

调用 `create_ma_campaign` 或 `update_ma_campaign` 之前，所有有实质影响的 `needs_confirmation` 项都必须解决。无实质影响的假设可以留在 `assumptions` 里，但必须在确认摘要中展示。

## 最少澄清原则

每轮只问一个问题：对受众、触发时机、通道、内容、频控或目标定义影响最大的那个未决决策。能用工具查清的事实，不要拿一长串问卷去问用户。
