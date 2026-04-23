# Tracking Principles

这是本地精简摘要，用于在 `wave-tracking-plan`、`wave-tracking`、`wave-sdk-integration` 中快速收敛埋点方案。

## 本地必须规则

- 优先记录业务事实而不是 UI 碎片；能在服务端稳定产生的关键结果，优先服务端上报。
- 事件命名要稳定、可长期维护；优先“通用事件名 + 属性区分细节”，不要为每个按钮单独造事件。
- 事件名在同一应用内保持统一风格；属性名统一 snake_case，布尔值优先 `is_` / `has_`。
- 事件属性描述本次行为上下文；用户属性描述用户长期或跨事件状态，不要混用。
- 同一属性跨事件保持类型一致；枚举值统一小写 snake_case；禁止动态属性名。
- SDK 已自动采集的预置事件和预置属性不要重复设计；单事件属性通常控制在 5–20 个。
- 登录、注册、跨设备、共享设备等场景不要只谈事件设计，必须同时补充用户标识方案。

## 官网权威入口

- 官方文档页 URL：
  [埋点方案选择](https://sensorswave.cn/docs/data-integration/tracking-strategy/)
- 对应 `llm.txt` URL：
  [tracking-strategy llm.txt](https://sensorswave.cn/docs/data-integration/tracking-strategy/llm.txt)

## 相关补充文档

- [数据模型](https://sensorswave.cn/docs/data-integration/data-model/)
  [llm.txt](https://sensorswave.cn/docs/data-integration/data-model/llm.txt)
- [事件和属性](https://sensorswave.cn/docs/data-integration/events-and-properties/)
  [llm.txt](https://sensorswave.cn/docs/data-integration/events-and-properties/llm.txt)
- [预置事件和预置属性](https://sensorswave.cn/docs/data-integration/preset-events-and-properties/)
  [llm.txt](https://sensorswave.cn/docs/data-integration/preset-events-and-properties/llm.txt)
- 用户标识专题：
  读取 [user-identification.md](user-identification.md)

## 使用说明

- 联网时，长文知识和细节口径优先参考官网文档页及对应 `llm.txt`。
- 无法联网时，退回本文件中的本地摘要规则继续推进。
