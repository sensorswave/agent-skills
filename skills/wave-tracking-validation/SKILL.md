---
name: wave-tracking-validation
description: >-
  在事件已经开始上报之后，对 Sensors Wave 埋点做质检。适用于把已发布的 Tracking Plan
  与实际数据对照、排查缺失事件或属性、做上线验收。Tracking Plan 写入/发布、SDK 接入
  或代码修复交给 wave-tracking。
---

# Wave 埋点质检

## 目标

以已发布的 Tracking Plan 为基线校验实际上报的事件数据，给出验收结论和具体的修复目标。

## 先加载

- 项目级 MCP 调用之前，先读 [policies/operating-rules.md](policies/operating-rules.md)。
- 需要确认措辞时，读 [prompts/interaction.md](prompts/interaction.md)。
- 调用质检工具之前，先读 [playbooks/tracking-validation.md](playbooks/tracking-validation.md)。

## 工具

- 基线：`list_tracking_plans`、`get_tracking_plan_detail`
- 质检：`get_tracking_plan_quality_check`
- 交叉验证：`list_events`、`list_event_properties`、`list_pipelines`

## 项目门禁

<!-- wave:project-gate -->
在调用其他项目级 MCP 工具前：

1. 调用 `list_projects`，展示 `project_id | name` 表格。
2. 等待用户回复数字 `project_id`。
3. 仅当本轮对话已经固定到一个项目，或用户明确说继续使用当前项目时，才跳过重新选择。

禁止静默挑选项目，也禁止在此步骤前调用质检或其他项目级工具。
<!-- /wave:project-gate -->

## 前置条件

- 用户必须已有项目和一份 Tracking Plan 基线。
- 计划应当在质检前已发布。未发布时，交给 `wave-tracking`。
- 如果改过代码，用户必须确认应用/服务已经重新构建/重新部署/重启。
- 用户必须确认关键事件已经开始上报。
- 用户必须明确要求开始质检。仅说「事件触发了」不算。

## 工作流

1. 先通过项目门禁，再确认计划。用户没给 plan id 时，列出计划让用户选择。
2. 确认计划状态；未发布时说明限制。
3. 确认运行时验证已完成，且用户明确同意开始质检。
4. 调用 `get_tracking_plan_quality_check`。
5. 把结果汇总成通过/失败加问题清单。问题按事件、属性、平台/Pipeline（如有）和可能的修复负责人分组。
6. 只在质检结果不明确或用户要求深入诊断时，才使用交叉验证工具。

## 边界

- 项目门禁未通过前，不要调用质检或其他项目级工具。
- 不要在这里修改 Tracking Plan、SDK 代码、Pipeline 设置或 Catalog 元数据。
- 在后续一轮质检确认之前，不要推断缺失的数据已经修好。
- 不要在这里做分析解读；趋势、漏斗、留存问题交给 `wave-analytics`，SQL 交给 `wave-sql-query`。

## 输出

返回：
- 验收结论：通过、失败，或因前置条件缺失而阻塞。
- 证据：计划 id/名称/状态和检查范围。
- 问题：缺失事件、缺失属性、近期无数据、取值覆盖异常，或仅部分实现。
- 下一步：把每个问题分别指向 `wave-tracking`、`wave-catalog-governance` 或 `wave-analytics`。

## 停止

汇报质检结果后停止。等用户决定是修埋点、更新 Catalog 元数据，还是做分析。
